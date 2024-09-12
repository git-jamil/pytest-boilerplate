# -*- coding: utf-8 -*-

import os
import pathlib
import warnings

import py
import pytest
import yaml

from devxhub_python.generate import generate_context
from devxhub_python.main import devxhub_python
from devxhub_python.prompt import prompt_for_config


class Result(object):
    """Holds the captured result of the devxhub_python project generation."""

    def __init__(self, exception=None, exit_code=0, project_dir=None, context=None):
        self.exception = exception
        self.exit_code = exit_code
        self.context = context
        self._project_dir = project_dir

    @property
    def project(self):
        """Return a py.path.local object if no exception occurred."""
        warning_message = (
            "project is deprecated and will be removed in a future release, "
            "please use project_path instead."
        )

        warnings.warn(
            warning_message,
            DeprecationWarning,
            stacklevel=1,
        )

        if self.exception is None:
            return py.path.local(self._project_dir)

        return None

    @property
    def project_path(self):
        """Return a pathlib.Path object if no exception occurred."""

        if self.exception is None:
            return pathlib.Path(self._project_dir)

        return None

    def __repr__(self):
        if self.exception:
            return "<Result {!r}>".format(self.exception)

        return "<Result {}>".format(self.project)


class boilerplate(object):
    """Class to provide convenient access to the devxhub_python API."""

    def __init__(self, template, output_factory, config_file):
        self._default_template = template
        self._output_factory = output_factory
        self._config_file = config_file
        self._counter = 0

    def _new_output_dir(self):
        dirname = "bake{:02d}".format(self._counter)
        output_dir = self._output_factory(dirname)
        self._counter += 1
        return output_dir

    def bake(self, extra_context=None, template=None):
        exception = None
        exit_code = 0
        project_dir = None
        context = None

        if template is None:
            template = self._default_template

        context_file = pathlib.Path(template) / "devxhub_python.json"

        try:
            # Render the context, so that we can store it on the Result
            context = prompt_for_config(
                generate_context(
                    context_file=str(context_file), extra_context=extra_context
                ),
                no_input=True,
            )

            # Run devxhub_python to generate a new project
            project_dir = devxhub_python(
                template,
                no_input=True,
                extra_context=extra_context,
                output_dir=str(self._new_output_dir()),
                config_file=str(self._config_file),
            )
        except SystemExit as e:
            if e.code != 0:
                exception = e
            exit_code = e.code
        except Exception as e:
            exception = e
            exit_code = -1

        return Result(
            exception=exception,
            exit_code=exit_code,
            project_dir=project_dir,
            context=context,
        )


@pytest.fixture(scope="session")
def _devxhub_python_config_file(tmpdir_factory):
    user_dir = tmpdir_factory.mktemp("user_dir")
    config_file = user_dir.join("config")

    config = {
        "devxhub_pythons_dir": str(user_dir.mkdir("devxhub_pythons")),
        "replay_dir": str(user_dir.mkdir("devxhub_python_replay")),
    }

    with config_file.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, Dumper=yaml.Dumper)

    return config_file


@pytest.fixture
def boilerplate(request, tmpdir, _devxhub_python_config_file):
    """Yield an instance of the boilerplate helper class that can be used to
    generate a project from a template.

    Run devxhub_python:
        result = boilerplate.bake(extra_context={
            'variable1': 'value1',
            'variable2': 'value2',
        })
    """
    template_dir = request.config.option.template

    output_dir = tmpdir.mkdir("boilerplate")
    output_factory = output_dir.mkdir

    yield boilerplate(template_dir, output_factory, _devxhub_python_config_file)

    # Add option to keep generated output directories.
    if not request.config.option.keep_baked_projects:
        output_dir.remove()


@pytest.fixture(scope="session")
def boilerplate_session(request, tmpdir_factory, _devxhub_python_config_file):
    """Yield an instance of the boilerplate helper class that can be used to
    generate a project from a template.

    Run devxhub_python:
        result = boilerplate.bake(extra_context={
            'variable1': 'value1',
            'variable2': 'value2',
        })
    """
    template_dir = request.config.option.template

    output_dir = tmpdir_factory.mktemp("boilerplate")
    output_factory = output_dir.mkdir

    yield boilerplate(template_dir, output_factory, _devxhub_python_config_file)

    # Add option to keep generated output directories.
    if not request.config.option.keep_baked_projects:
        output_dir.remove()


def pytest_addoption(parser):
    group = parser.getgroup("boilerplate")
    group.addoption(
        "--template",
        action="store",
        default=".",
        dest="template",
        help="specify the template to be rendered",
        type=str,
    )

    group.addoption(
        "--keep-baked-projects",
        action="store_true",
        default=False,
        dest="keep_baked_projects",
        help="Keep projects directories generated with 'boilerplate.bake()'.",
    )


def pytest_configure(config):
    # To protect ourselves from tests or fixtures changing directories, keep
    # an absolute path to the template.
    config.option.template = os.path.abspath(config.option.template)
