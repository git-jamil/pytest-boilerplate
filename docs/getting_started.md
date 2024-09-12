# Installation

**pytest-boilerplate** is available for download from [PyPI] via [pip]:

```no-highlight
$ pip install pytest-boilerplate
```

It will automatically install [pytest] along with [devxhub_python].

  [PyPI]: https://pypi.python.org/pypi
  [devxhub_python]: https://github.com/devxhub_python/devxhub_python
  [pip]: https://pypi.python.org/pypi/pip/
  [pytest]: https://github.com/pytest-dev/pytest

# Usage

The ``boilerplate.bake()`` method generates a new project from your template based on the
default values specified in ``devxhub_python.json``:

```python
def test_bake_project(boilerplate):
    result = boilerplate.bake(extra_context={'repo_name': 'helloworld'})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'helloworld'
    assert result.project.isdir()
```

It accepts the ``extra_context`` keyword argument that will be
passed to devxhub_python. The given dictionary will override the default values
of the template context, allowing you to test arbitrary user input data.

Please see the [Injecting Extra Context] section of the
official devxhub_python documentation.

  [Injecting Extra Context]: https://devxhub_python.readthedocs.io/en/latest/advanced/injecting_context.html#injecting-extra-context
