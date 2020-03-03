# Download minion installer
# Installer version for Linux is specified in the cmd to execute the bootstrap
# Installer version for Windows is specified by the installer used, 2019.2.0-Py3
get_installer:
  file.managed:
  {% if grains['kernel'] == 'Linux' %}
    - name: /tmp/install_salt.sh
    - source: salt://updatesalt/files/bootstrap-salt.sh
    - mode: 500
  {% elif grains['kernel'] == 'Windows' %}
    - name: 'C:\\salt-minion-2019.2.0-py3.exe'
    - source: http://repo.saltstack.com/windows/Salt-Minion-2019.2.0-Py3-AMD64-Setup.exe
    - skip_verify: true
  {% endif %}
