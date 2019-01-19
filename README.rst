==========================
logging-formatter-anticrlf
==========================
--------------------------------------------------------------------------
Python logging Formatter for CRLF Injection (CWE-93 / CWE-117) prevention
--------------------------------------------------------------------------

logging Formatter to sanitize CRLF errors (CWE-93, some forms of CWE-117)

This class is a drop-in replacement for ``logging.Formatter``, and has the
exact same construction arguments. However, as a final step of formatting a
log line, it escapes carriage returns (\\r) and linefeeds (\\n).

By default, these are replaced with their escaped equivalents (see `Examples`_),
but the ``replacements`` dictionary can be modified to change this behavior.

This sanitization should solve CWE-93 errors and CRLF-based versions of
CWE-117. Some CWE-117 errors are concerns about e.g. XSS flaws in logs that
are likely to be viewed in a browser; this formatter can't handle every
form of CWE-117.

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


Changing Replacements
=====================

The ``replacements`` field of the formatter is a ``SubstitutionMap`` object that behaves
like a ``dict`` with a few exceptions designed to help developers avoid making insecure mistakes.

Specifically:

* an "empty" ``SubstitutionMap`` object will contain the default mappings for CR and LF chars
* calling ``del`` on either the CR or LF key will *reset the value* rather than *delete* the key
* any attempt to create a key-value pair that results in any value containing any of the keys
  will raise an ``UnsafeSubstitutionError``

The rationale for the last item is that the keys of the ``replacements`` field are strings
that are considered unsafe. Replacing one unsafe string with another defeats the purpose of
using this module.

Additionally, if you assign a regular ``dict`` to the ``replacements`` field, and try to log
something using that configuration, ``anticrlf.LogFormatter`` will reset the ``replacements``
field to its default value and issue a ``UserWarning`` to that effect.

That means the following::

    formatter.replacements["\n"] = "\\x0A"  # replace LF chars with '\x0A'
    del formatter.replacements["\n"]        # return to replacing LF with '\n'
    formatter.replacements["\t"] = "\\t"    # replace tabs with '\t'
    formatter.replacements["\n"] = "<\t>"   # raises UnsafeSubstitutionError

The last occurs because the value ``<\t>`` contains ``\t``, which was previously created as a key.

And::

    formatter.replacements = { "\n": "\r" }  # this is a mistake!
    logger.info("example")

Will result, if that logger is using that formatter, in ``replacements`` being returned to its
safe default value and a ``UserWarning`` about that being issued.
