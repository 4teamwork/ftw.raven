.. contents:: Table of Contents


Purpose
=======

This package extends `raven`, the Sentry integration with
a Plone integration wich is not logger based but hooks into
the Zope exception handling.

Be aware that there is already a standard `logging based Zope /
Plone integration for raven <https://docs.getsentry.com/hosted/clients/python/integrations/zope/>`_. You should use the standard implementation unless you
want the exception hook based integration.


Installation and configuration
==============================

- Add the `ftw.raven` package to your dependencies.
- Configure the raven client with environment variables in buildout

Example configuration for buildout:

.. code:: ini

    [instance]
    eggs +=
        ftw.raven
    environment-vars +=
        RAVEN_DSN https://123:456@sentry.local/2


Configuration-Test
==================

You can test your configuration by visiting the view ``raven-test`` on
any context as ``Manager``-user.
This will trigger an exception which should appear in your sentry project.

Note that it's possible that the trigger doesn't work on local test systems in
some cases.

In JavaScript you can call the function ``raven_test()`` in your javascript
console, which will also trigger an exception.


Release tracking
================

When an exception is reported, the release can be sent along.
A release can either be the version number of a released distribution
(e.g. released on pypi) or the HEAD SHA of a project checkout when the
app is not released on pypi.

Version of a released distribution
----------------------------------

For using a distribution version as release, the environment variable
``RAVEN_PROJECT_DIST`` must contain the name of the distribution, e.g.

.. code:: ini

    [instance]
    environment-vars +=
        RAVEN_PROJECT_DIST my.project


Git SHA of checkout
-------------------

Usually the buildout root is a checkout of the project, thus we need to
configured the ``RAVEN_BUILDOUT_ROOT`` so that the git repository is found:

.. code:: ini

    [instance]
    environment-vars +=
        RAVEN_BUILDOUT_ROOT ${buildout:directory}


Ignored exceptions
==================

By default, not all exceptions are reported, because some exceptions
such as redirects or 404s are not errors but are implemented as exceptions.
Without configuration, the exceptions ``NotFound``, ``Unauthorized``,
``Redirect`` and ``Intercepted``.

Reporting of those exceptions can be enabled by with the environment variable
``RAVEN_ENABLE_EXCEPTIONS``:

.. code::

    [instance]
    environment-vars +=
        RAVEN_ENABLE_EXCEPTIONS NotFound, Redirect

If you need to disable custom exceptions, you can do that with the environment
variable ``RAVEN_DISABLE_EXCEPTIONS``:

.. code::

    [instance]
    environment-vars +=
        RAVEN_DISABLE_EXCEPTIONS UnimportantError


Report JavaScript errors
========================

In order to be able to report JavaScript-errors, the ``ftw.raven:default``
Generic Setup profile must be installed, which registers a JavaScript
including the raven library and the configuration.


Additional tags
===============

It is possible to report additional, predefined tags for a deployment.
The tags may be directly declared as JSON in the environment variable
``RAVEN_TAGS`` or the variable ``RAVEN_TAGS_FILE`` may contain a path
to a json-file.
These two methods may be combined, and the respective dictionaries will
be merged (with tags from the ``RAVEN_TAGS`` variable taking precedence).

The JSON must be a one-level hash containing strings as keys and values.

Examples:

.. code::

    [instance]
    environment-vars +=
        RAVEN_TAGS {"deployment": "production"}

.. code::

    [instance]
    environment-vars +=
        RAVEN_TAGS_FILE ${buildout:directory}/conf/raven_tags.json


Links
=====

- Github: https://github.com/4teamwork/ftw.raven
- Issues: https://github.com/4teamwork/ftw.raven/issues
- Pypi: http://pypi.python.org/pypi/ftw.raven
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.raven

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.raven`` is licensed under GNU General Public License, version 2.
