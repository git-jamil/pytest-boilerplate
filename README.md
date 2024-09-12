# pytest-boilerplate

[pytest][pytest] is a mature testing framework for Python that is developed
by a thriving and ever-growing community of volunteers. It uses plain assert
statements and regular Python comparisons. At the core of the pytest test
framework is a powerful hook-based plugin system.

**pytest-boilerplate** is a pytest plugin that comes with a ``boilerplate`` fixture
which is a wrapper for the [devxhub_python][devxhub_python] API for generating
projects. It helps you verify that your template is working as expected and
takes care of cleaning up after running the tests. 🍪

# Installation

**pytest-boilerplate** is available for download from [PyPI][pypi] via [pip][pip]:

```text
pip install pytest-boilerplate
```
This will automatically install [pytest][pytest] and
[devxhub_python][devxhub_python].

# Usage

## Generate a new project

The ``boilerplate.bake()`` method generates a new project from your template
based on the default values specified in ``devxhub_python.json``:

```python
def test_bake_project(boilerplate):
    result = boilerplate.bake(extra_context={"repo_name": "helloworld"})

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "helloworld"
    assert result.project_path.is_dir()

    # The `project` attribute is deprecated
    assert result.project.basename == "helloworld"
    assert result.project.isdir()
```

**Please note that the `project` attribute of the returned `Result` class is
deprecated and will be removed in a future release, please use `project_path`
instead.**

The ``boilerplate.bake()`` method also accepts the ``extra_context`` keyword
argument that will be passed to devxhub_python. The given dictionary will
override the default values of the template context, effectively allowing you
to test arbitrary user input data.

For more information on injecting extra context, please check out the
[devxhub_python documentation][extra-context].

## Specify the template directory

By default ``boilerplate.bake()`` looks for a devxhub_python template in the
current directory. This can be overridden on the command line by passing a
``--template`` parameter to pytest:

```text
pytest --template TEMPLATE
```

You can customize the devxhub_python template directory from a test by passing
in the optional ``template`` paramter:

```python
@pytest.fixture
def custom_template(tmpdir):
    template = tmpdir.ensure("devxhub_python-template", dir=True)
    template.join("devxhub_python.json").write('{"repo_name": "example-project"}')

    repo_dir = template.ensure("{{devxhub_python.repo_name}}", dir=True)
    repo_dir.join("README.rst").write("{{devxhub_python.repo_name}}")

    return template


def test_bake_custom_project(boilerplate, custom_template):
    """Test for 'devxhub_python-template'."""
    result = boilerplate.bake(template=str(custom_template))

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "example-project"
    assert result.project_path.is_dir()
```

## Keep output directories for debugging

By default ``boilerplate`` removes baked projects.

However, you can pass the ``keep-baked-projects`` flag if you'd like to keep
them ([it won't clutter][temporary-directories] as pytest only keeps the
three newest temporary directories):

```text
pytest --keep-baked-projects
```

# Community

Contributions are very welcome! If you encounter any problems, please [file
an issue][new-issue] along with a detailed description. Tests can be run with
[tox][tox]. Please make sure all of the tests are green before you submit a
pull request.

You can also support the development of this project by volunteering to
become a maintainer, which means you will be able to triage issues, merge
pull-requests, and publish new releases. If you're interested, please submit
a pull-request to add yourself to the list of [maintainers][community] and
we'll get you started! 🍪

Please note that **pytest-boilerplate** is released with a [Contributor Code of
Conduct][code-of-conduct]. By participating in this project you agree to
abide by its terms.

# License

Distributed under the terms of the [MIT license][license], **pytest-boilerplate**
is free and open source software.

[devxhub_python]: https://github.com/devxhub/dxh-py
[pytest]: https://github.com/pytest-dev/pytest
[pip]: https://pypi.org/project/pip/
[pypi]: https://pypi.org/project/pytest-boilerplate/
[extra-context]: https://devxhub_python.readthedocs.io/en/latest/advanced/injecting_context.html
[temporary-directories]: https://docs.pytest.org/en/latest/tmpdir.html#the-default-base-temporary-directory
[tox]: https://pypi.org/project/tox/
[new-issue]: https://github.com/devxhub/pytest-boilerplate/issues
[code-of-conduct]: https://github.com/devxhub/pytest-boilerplate/blob/main/CODE_OF_CONDUCT.md
[community]: https://github.com/devxhub/pytest-boilerplate/blob/main/COMMUNITY.md
[license]: https://github.com/devxhub/pytest-boilerplate/blob/main/LICENSE
