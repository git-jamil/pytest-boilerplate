# -*- coding: utf-8 -*-

import collections
import json

import pytest

pytest_plugins = "pytester"


@pytest.fixture(name="django_boilerplate")
def fixture_django_boilerplate_template(tmpdir):
    template = tmpdir.ensure("django-boilerplate", dir=True)

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
