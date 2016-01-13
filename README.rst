.. contents:: Table of Contents


Purpose
=======

This package extends `raven`, the Sentry integration with
a Plone integration wich is not logger based but hooks into
the Zope exception handling.


Installation and configuration
==============================

- Add the `ftw.raven` package to your dependencies.
- Configure the client with ZCML, preferrably in buildout.

Example configuration for buildout:

.. code:: ini

    [instance]
    eggs += ftw.raven
    zcml-additional =
        <configure xmlns:raven="http://ns.4teamwork.ch/raven">
            <include package="ftw.raven" />
            <raven:config dsn="https://123:456@sentry.local/2" />
        </configure>


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
