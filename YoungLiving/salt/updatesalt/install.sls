# Execute minion installation
update_salt_minion:
  cmd.run:
  {%- if grains['kernel'] == 'Linux' -%}
    - name: sh /tmp/install_salt.sh -x python3 stable 2019.2.0
  {%- elif grains['kernel'] == 'Windows' -%}
    - name: 'C:\\salt-minion-2019.2.0-py3.exe /S'
  {%- endif -%}
    - bg: true
