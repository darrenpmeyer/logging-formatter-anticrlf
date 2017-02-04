"""tests for anticrlf.LogFormatter"""
import pytest

from anticrlf import LogFormatter

from io import StringIO
from imp import reload
import logging


@pytest.fixture()
def logbundle():
    logging.shutdown()
    reload(logging)

    strio = StringIO()

    formatter = LogFormatter('%(message)s')
    handler = logging.StreamHandler(strio)
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger, strio, formatter


def test_lf(logbundle):
    (logger, strio, formatter) = logbundle
    logger.info("Test\nitem")
    assert "Test\\nitem\n" == strio.getvalue()


def test_cr(logbundle):
    (logger, strio, formatter) = logbundle
    logger.info("Test\ritem")
    assert "Test\\ritem\n" == strio.getvalue()


def test_custom_sep(logbundle):
    (logger, strio, formatter) = logbundle
    formatter.replacements["\n"] = "^"
    logger.info("Test\n\nitem")
    assert "Test^^item\n" == strio.getvalue()
