# Download minion installer
# Installer version for Linux is specified in the cmd to execute the bootstrap
# Run:
# curl -L https://bootstrap.saltstack.com -o /srv/salt/minion_update/files/install_salt.sh
# Installer version for Windows is specified by the installer used, 2019.2.3-Py3
get_installer:
  file.managed:
  {% if grains['kernel'] == 'Linux' %}
    - name: /tmp/install_salt.sh
    - source: salt://updatesalt/files/install_salt.sh
    - mode: 500
  {% elif grains['kernel'] == 'Windows' %}
    - name: 'C:\\salt-minion-2019.2.3-py3.exe'
    - source: http://repo.saltstack.com/windows/Salt-Minion-2019.2.3-Py3-AMD64-Setup.exe
    - skip_verify: true
  {% endif %}


# Execute minion installation
update_salt_minion:
  cmd.run:
  {% if grains['kernel'] == 'Linux' %}
# note:  -F switch required by RHEL/CentOS to replace the repo file
    - name: sh /tmp/install_salt.sh -F -x python3 stable 2019.2.3
  {% elif grains['kernel'] == 'Windows' %}
    - name: 'C:\\salt-minion-2019.2.3-py3.exe /S'
  {% endif %}
    - bg: true
