# -*- coding: utf-8 -*-


def test_boilerplate_group(testdir):
    result = testdir.runpytest("--help")
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["boilerplate:", "*--template=TEMPLATE*"])
