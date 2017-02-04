==========================
logging-formatter-anticrlf
==========================
---------------------------------------------------------------
Python logging Formatter for CRLF Injection (CWE-93) prevention
---------------------------------------------------------------

logging Formatter to sanitize CRLF errors (CWE-93)

This class is a drop-in replacement for ``logging.Formatter``, and has the
exact same construction arguments. However, as a final step of formatting a
log line, it escapes carriage returns (\\r) and linefeeds (\\n).

By default, these are replaced with their escaped equivalents (see `Examples`_),
but the ``replacements`` dictionary can be modified to change this behabior.

Installation
============

::

    pip install logging-formatter-anticrlf


Examples
========

::

    import anticrlf

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(anticrlf.LogFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info("Example text with a newline\nhere")

This results in::

    2017-02-03 08:43:52,557 - __main__ - INFO - Example text with a newline\nhere

Whereas with the default ``Formatter``, it would be::

    2017-02-03 08:43:52,557 - __main__ - INFO - Example text with a newline
    here

If you wanted newlines to be replaced with \\x0A instead, you could::

    formatter = anticrlf.LogFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter.replacements["\n"] = "\\x0A"  # Note the double backslash for literal!
    handler.setFormatter(formatter)
