get_bootstrap:
  file.managed:
    - name: /tmp/bootstrap-salt.sh
    - source: salt://updatesalt/bootstrap-salt.sh
    - mode: 500
