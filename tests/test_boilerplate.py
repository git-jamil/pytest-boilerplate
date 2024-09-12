# -*- coding: utf-8 -*-

import json
import pytest


def test_boilerplate_fixture(testdir):
    """Make sure that pytest accepts the `boilerplate` fixture."""

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_valid_fixture(boilerplate):
            assert hasattr(boilerplate, 'bake')
            assert callable(boilerplate.bake)
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_valid_fixture PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_boilerplate_bake_with_template_kwarg(testdir, django_boilerplate):
    """bake accepts a template kwarg."""
    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_project(boilerplate):
            result = boilerplate.bake(
                extra_context={'repo_name': 'helloworld'},
                template=r'%s',
            )

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'helloworld'
            assert result.project.isdir()

            assert str(result) == '<Result {}>'.format(result.project)
    """
        % django_boilerplate
    )

    # run pytest without the template cli arg
    result = testdir.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_boilerplate_bake_template_kwarg_overrides_cli_option(
    testdir, django_boilerplate
):
    """bake template kwarg overrides cli option."""

    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_project(boilerplate):
            result = boilerplate.bake(
                extra_context={'repo_name': 'helloworld'},
                template=r'%s',
            )

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'helloworld'
            assert result.project.isdir()

            assert str(result) == '<Result {}>'.format(result.project)
    """
        % django_boilerplate
    )

    # run pytest with a bogus template name
    # it should use template directory passed to `boilerplate.bake`
    result = testdir.runpytest("-v", "--template=foobar")

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_boilerplate_bake(testdir, django_boilerplate):
    """Programmatically create a **devxhub_python** template and use `bake` to
    create a project from it.
    """
    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_project(boilerplate):
            result = boilerplate.bake(extra_context={'repo_name': 'helloworld'})

            assert result.exit_code == 0
            assert result.exception is None

            assert result.project_path.name == 'helloworld'
            assert result.project_path.is_dir()
            assert str(result) == '<Result {}>'.format(result.project_path)

            assert result.project.basename == 'helloworld'
            assert result.project.isdir()
            assert str(result) == '<Result {}>'.format(result.project)
    """
    )

    result = testdir.runpytest("-v", "--template={}".format(django_boilerplate))

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_boilerplate_bake_project_warning(testdir, django_boilerplate):
    """Programmatically create a **devxhub_python** template and use `bake` to
    create a project from it and check for warnings when accesssing the project
    attribute.
    """
    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-
        import warnings

        def test_bake_project(boilerplate):
            warning_message = (
                "project is deprecated and will be removed in a future release, "
                "please use project_path instead."
            )

            result = boilerplate.bake(extra_context={'repo_name': 'helloworld'})

            assert result.exit_code == 0
            assert result.exception is None

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                project_basename = result.project.basename

            assert project_basename == 'helloworld'

            [warning] = w
            assert issubclass(warning.category, DeprecationWarning)
            assert str(warning.message) == warning_message

            assert str(result) == '<Result {}>'.format(result.project)
    """
    )

    result = testdir.runpytest("-v", "--template={}".format(django_boilerplate))

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_boilerplate_bake_result_context(testdir, django_boilerplate):
    """Programmatically create a **devxhub_python** template and use `bake` to
    create a project from it.

    Check that the result holds the rendered context.
    """

    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        import collections

        def test_bake_project(boilerplate):
            result = boilerplate.bake(extra_context=collections.OrderedDict([
                ('repo_name', 'boilerplate'),
                ('short_description', '{{devxhub_python.repo_name}} is awesome'),
            ]))

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'boilerplate'
            assert result.project.isdir()

            assert result.context == {
                'repo_name': 'boilerplate',
                'short_description': 'boilerplate is awesome',
            }

            assert str(result) == '<Result {}>'.format(result.project)
    """
    )

    result = testdir.runpytest("-v", "--template={}".format(django_boilerplate))

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_boilerplate_bake_result_context_exception(testdir, django_boilerplate):
    """Programmatically create a **devxhub_python** template and use `bake` to
    create a project from it.

    Check that exceptions resulting from rendering the context are stored on
    result and that the rendered context is not set.
    """

    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        import collections

        def test_bake_project(boilerplate):
            result = boilerplate.bake(extra_context=collections.OrderedDict([
                ('repo_name', 'boilerplate'),
                ('short_description', '{{devxhub_python.nope}}'),
            ]))

            assert result.exit_code == -1
            assert result.exception is not None
            assert result.project is None

            assert result.context is None

            assert str(result) == '<Result {!r}>'.format(result.exception)
    """
    )

    result = testdir.runpytest("-v", "--template={}".format(django_boilerplate))

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_boilerplate_bake_should_create_new_output_directories(
    testdir, django_boilerplate
):
    """Programmatically create a **devxhub_python** template and use `bake` to
    create a project from it.
    """
    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_should_create_new_output(boilerplate):
            first_result = boilerplate.bake()
            assert first_result.exception is None
            assert first_result.project.dirname.endswith('bake00')

            second_result = boilerplate.bake()
            assert second_result.exception is None
            assert second_result.project.dirname.endswith('bake01')
    """
    )

    result = testdir.runpytest("-v", "--template={}".format(django_boilerplate))

    result.stdout.fnmatch_lines(["*::test_bake_should_create_new_output PASSED*"])


def test_boilerplate_fixture_removes_output_directories(testdir, django_boilerplate):
    """Programmatically create a **devxhub_python** template and use `bake` to
    create a project from it.
    """
    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-
        import os

        def test_to_create_result(boilerplate):
            global result_dirname
            result = boilerplate.bake()
            result_dirname = result.project.dirname
            assert result.exception is None

        def test_previously_generated_directory_is_removed(boilerplate):
            exists = os.path.isdir(result_dirname)
            assert exists is False
    """
    )

    result = testdir.runpytest("-v", "--template={}".format(django_boilerplate))

    result.stdout.fnmatch_lines(
        [
            "*::test_to_create_result PASSED*",
            "*::test_previously_generated_directory_is_removed PASSED*",
        ]
    )


def test_boilerplate_fixture_doesnt_remove_output_directories(
    testdir, django_boilerplate
):
    """Programmatically create a **devxhub_python** template and use `bake` to
    create a project from it.
    """
    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-
        import os

        def test_to_create_result(boilerplate):
            global result_dirname
            result = boilerplate.bake()
            result_dirname = result.project.dirname
            assert result.exception is None

        def test_previously_generated_directory_is_not_removed(boilerplate):
            exists = os.path.isdir(result_dirname)
            assert exists is True
    """
    )

    result = testdir.runpytest(
        "-v", "--template={}".format(django_boilerplate), "--keep-baked-projects"
    )

    result.stdout.fnmatch_lines(
        [
            "*::test_to_create_result PASSED*",
            "*::test_previously_generated_directory_is_not_removed PASSED*",
        ]
    )


def test_boilerplate_bake_should_handle_exception(testdir):
    """Programmatically create a **devxhub_python** template and make sure that
    boilerplate.bake() handles exceptions that happen during project generation.

    We expect **devxhub_python** to raise a `NonTemplatedInputDirException`.
    """
    template = testdir.tmpdir.ensure("devxhub_python-fail", dir=True)

    template_config = {"repo_name": "foobar", "short_description": "Test Project"}
    template.join("devxhub_python.json").write(json.dumps(template_config))

    template.ensure("devxhub_python.repo_name", dir=True)

    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_should_fail(boilerplate):
            result = boilerplate.bake()

            assert result.exit_code == -1
            assert result.exception is not None
            assert result.project is None
    """
    )

    result = testdir.runpytest("-v", "--template={}".format(template))

    result.stdout.fnmatch_lines(["*::test_bake_should_fail PASSED*"])


@pytest.mark.parametrize("choice", ["mkdocs", "sphinx", "none"])
def test_boilerplate_bake_choices(testdir, choice):
    """Programmatically create a **devxhub_python** template and make sure that
    boilerplate.bake() works with choice variables.
    """
    template = testdir.tmpdir.ensure("devxhub_python-choices", dir=True)
    template_config = {"repo_name": "docs", "docs_tool": ["mkdocs", "sphinx", "none"]}
    template.join("devxhub_python.json").write(json.dumps(template_config))

    repo = template.ensure("{{devxhub_python.repo_name}}", dir=True)
    repo.join("README.rst").write("docs_tool: {{devxhub_python.docs_tool}}")

    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_project(boilerplate):
            result = boilerplate.bake(
                extra_context={'docs_tool': '%s'},
                template=r'%s',
            )

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'docs'
            assert result.project.isdir()

            assert result.project.join('README.rst').read() == 'docs_tool: %s'

            assert str(result) == '<Result {}>'.format(result.project)
    """
        % (choice, template, choice)
    )

    # run pytest without the template cli arg
    result = testdir.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])

    result = testdir.runpytest("-v", "--template={}".format(template))
