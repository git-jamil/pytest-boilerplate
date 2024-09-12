# -*- coding: utf-8 -*-

import collections
import json

import pytest

pytest_plugins = "pytester"


@pytest.fixture(name="devxhub_python_template")
def fixture_devxhub_python_template(tmpdir):
    template = tmpdir.ensure("devxhub_python-template", dir=True)

    template_config = collections.OrderedDict(
        [("repo_name", "foobar"), ("short_description", "Test Project")]
    )
    template.join("devxhub_python.json").write(json.dumps(template_config))

    template_readme = "\n".join(
        [
            "{{devxhub_python.repo_name}}",
            "{% for _ in devxhub_python.repo_name %}={% endfor %}",
            "{{devxhub_python.short_description}}",
        ]
    )

    repo = template.ensure("{{devxhub_python.repo_name}}", dir=True)
    repo.join("README.rst").write(template_readme)

    return template
