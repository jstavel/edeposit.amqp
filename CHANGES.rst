Changelog
=========

1.8.16
------
    - .ack() simplified once more.

1.8.15
------
    - .ack() now doesn't use shared property to signal ack tag.

1.8.13
------
    - Added log output in case of exception.

1.8.12
------
    - Fixed metadata in setup.py.

1.8.11
------
    - Added bindigs for https://github.com/edeposit/edeposit.amqp.aleph_link_export.

1.8.10
------
    - Fixed missing requirement to edeposit.aqmp.serializers.

1.8.0 - 1.8.9
-------------
    - Added ``send_back()`` callback, which is now given to all ``reactToAMQPMessage()``. All packages was changed to support this. See #40 for details.
    - Added bindigs for https://github.com/edeposit/edeposit.amqp.downloader.
    - Fixed sys.argv parsing bug in some of the daemon scripts.
    - Fixed bug in daemonwrapper.
    - Quick fix of the problem with supervisord and DaemonRunner (see #41).
    - Added bindigs for https://github.com/edeposit/edeposit.amqp.storage.
    - Added update_templates.sh. Relationship diagram migrated to template system.
    - setup.py improved.
    - ``settings.py`` updated.
    - Removed dependencies to subprojects. They are now in special meta package `edeposit.amqp.meta <https://github.com/edeposit/edeposit.amqp.meta>`_.
    - Added bindigs for https://github.com/edeposit/edeposit.amqp.marcxml2mods.
    - Fixed bug in marcxml2modsd.py.
    - Fixed bug in ``edeposit_amqp_ltpd.py``.
    - Fixed bug in ``docs/__init__.py``.

1.7.0 - 1.7.3
-------------
    - Fixed problems with virtualenv.
    - Added AMQP bindings for https://github.com/edeposit/edeposit.amqp.pdfgen.
    - Dependecy to python-daemon frozen at 1.6 to fix virtualenv problems.
    - Added docstring for AMQPDaemon.process_exception().

1.6.0 - 1.6.2
-------------
    - Added bindings for https://github.com/edeposit/edeposit.amqp.ltp.
    - Documentation updated.
    - Fixed bugs in package system / manifest.

1.5.0 - 1.5.3
-------------
    - Added bindings for https://github.com/edeposit/edeposit.amqp.harvester.
    - Added bindings for https://github.com/edeposit/edeposit.amqp.edeposit.amqp.antivirus.
    - Fixed bug in setup.py (missing link to script in ``/bin``).
    - Experimental change in daemonwrapper module.

1.4.0 - 1.4.1
-------------
    - Fixed bug in setup.py.
    - Scripts moved to ``/bin`` directory. They will be put to ``$PATH`` when package is installed, so users won't need too call them with full path.
    - Added bindings for https://github.com/edeposit/edeposit.amqp.ftp.
    - Documentation improved.
    - Added new amqp tool.
    - Tests migrated to pytest.
    - Fixed some bugs.

1.3.0 - 1.3.3
-------------
    - Added tracebacks to the headers, if the exception is thrown.
    - ``RABBITMQ_ALEPH_DAEMON_QUEUE`` renamed to ``RABBITMQ_ALEPH_INPUT_QUEUE``
    - ``RABBITMQ_ALEPH_PLONE_QUEUE`` renamed to ``RABBITMQ_ALEPH_OUTPUT_QUEUE``
    - ``RABBITMQ_ALEPH_DAEMON_KEY`` renamed to ``RABBITMQ_ALEPH_INPUT_KEY``.
    - ``RABBITMQ_ALEPH_PLONE_KEY`` renamed to ``RABBITMQ_ALEPH_OUTPUT_KEY``.
    - Unicode added to allowed types in settings.py.
    - Added bindings for https://github.com/edeposit/edeposit.amqp.calibre.
    - Version of package and documentation is now automatically parsed from this file.
    - Images in documentation were downloaded to ``_static``.
    - Changed internal way of handling AMQP communication. This shouldn't change user API.
    - Documentation updated to reflect changes in internal API. Added UML diagrams.

1.2.0 - 1.2.2
-------------
    - Documentation updated. Added intersphinx links to edeposit.amqp.serializers.
    - edeposit.amqp.serializers API changed, so this module needed to be adjusted.
    - Serialization is now handled (but not stored) in this module, instead of aleph. It will be used in other modules too.
    - Added bindings for https://github.com/edeposit/edeposit.amqp.serializers.

1.1.5 - 1.1.6
-------------
    - Documentation is now even for settings.py's attributes.
    - User defined JSON configuration is now supported.
    - Added autogeneration of documentation to the package generator (setup.py).

1.1.0
-----
    - Project released at PYPI

1.0 (unreleased)
----------------
    - alephdaemon is working correctly, other classes are in release state too