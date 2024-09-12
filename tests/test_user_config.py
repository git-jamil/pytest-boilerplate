# -*- coding: utf-8 -*-


def test_config(testdir):
    """Make sure that pytest accepts the `boilerplate` fixture."""

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        # -*- coding: utf-8 -*-

        import yaml


        def test_user_dir(tmpdir_factory, _devxhub_python_config_file):
            basetemp = tmpdir_factory.getbasetemp()

            assert _devxhub_python_config_file.basename == 'config'

            user_dir = _devxhub_python_config_file.dirpath()
            assert user_dir.fnmatch('user_dir?')

            assert user_dir.dirpath() == basetemp


        def test_valid_devxhub_python_config(_devxhub_python_config_file):
            with open(_devxhub_python_config_file) as f:
                config = yaml.load(f, Loader=yaml.Loader)

            user_dir = _devxhub_python_config_file.dirpath()

            expected = {
                'devxhub_pythons_dir': str(user_dir.join('devxhub_pythons')),
                'replay_dir': str(user_dir.join('devxhub_python_replay')),
            }
            assert config == expected
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        ["*::test_user_dir PASSED*", "*::test_valid_devxhub_python_config PASSED*"]
    )

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
