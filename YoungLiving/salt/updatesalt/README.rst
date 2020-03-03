====
updatesalt
====
Formula to install update Salt Minion to python3

.. note::

    See the full `Salt Formulas installation and usage instructions
    <http://docs.saltstack.com/topics/development/conventions/formulas.html>`_.

Available states
================

- updatesalt
- updatesalt.show_version
- updatesalt.get_installer
- updatesalt.install


``updatesalt``
---------
Default state will install Salt Minion for Python3

``Sample output``
---------

yl-minion1:
----------
          ID: show_version
    Function: test.configurable_test_state
        Name: show version
      Result: True
     Comment: 2019.2.0
     Started: 20:38:26.948408
    Duration: 0.464 ms
     Changes:
----------
          ID: get_installer
    Function: file.managed
        Name: /tmp/install_salt.sh
      Result: True
     Comment: File /tmp/install_salt.sh is in the correct state
     Started: 20:38:26.952053
    Duration: 36.097 ms
     Changes:
----------
          ID: update_salt_minion
    Function: cmd.run
        Name: sh /tmp/install_salt.sh -x python3 stable 2019.2.3
      Result: True
     Comment: Command "sh /tmp/install_salt.sh -x python3 stable 2019.2.3" run
     Started: 20:38:26.988934
    Duration: 12.865 ms
     Changes:
              ----------
              pid:
                  21925
              retcode:
                  None
              stderr:
              stdout:
