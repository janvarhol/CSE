################################################################
# This state is meant to be run on the minion needing a new cert
################################################################
{% set minion_interfaces = grains.hwaddr_interfaces %}
test_mac_check_pillar:
  test.check_pillar:
    - present: mac
    - failhard: true

{% set minion_mac = salt['pillar.get']('mac') %}


{% for interface in minion_interfaces %}
{% set test_mac = minion_interfaces[interface].replace(':','') %}
# test_{{ interface }}:
#   test.succeed_without_changes:
#     - name: test interface output for {{ interface }} - {{ minion_interfaces[interface] }}

{% if minion_mac.upper() == test_mac.upper() %}
{#
test_mac_{{ interface }}:
  test.succeed_without_changes:
    - name: FOUND MATCH minion_mac={{ minion_mac }} mac from grain={{ minion_interfaces[interface] }}
#}

{% if interface.startswith('w') %}
{% set connection_id = 'wireless-ebay-corp' %}
{% else %}
{% set connection_id = 'wired-ebay-corp' %}
{% endif %}

{% if grains.os == "Ubuntu" and grains.osrelease == "14.04" %}
{% set uuid = salt['cmd.run']('uuidgen') %}
setup_nm:
  file.managed:
    - name: /etc/NetworkManager/system-connections/wired-ebay-corp
    - source: salt://minion/files/wired-ebay-corp.tpl
    - user: root
    - group: root
    - mode: 600
    - template: jinja
    - uuid: {{ uuid }}

pause_nm:
  module.run:
    - name: test.sleep
    - length: 3
{% else %}
setup_nm:
  nmcli.connection_exists:
    - name: {{ connection_id }}
    - interface: {{ interface }}
    - crt_path: /etc/pki/salt/802.1x.crt
    - key_path: /etc/pki/salt/{{ grains.id }}.key
    - key_password: {{ pillar.get('nm_key_pass') }}
{% endif %}

fix_managed:
  file.replace:
    - name: /etc/NetworkManager/NetworkManager.conf
    - pattern: managed=false
    - repl: managed=true

pause_up_nm:
  module.run:
    - name: test.sleep
    - length: 3
    - onchanges:
      - setup_nm

# salt <minion_id> nmcli.up_connection wired-ebay-corp
up_connection:
  # module.run:
  #   - name: nmcli.up_connection
  #   - connection_id: {{ connection_id }}
  #   - require:
  #     - setup_nm
  nmcli.connection_up:
    - name: {{ connection_id}}
    - require:
      - setup_nm


{% break %}
{% endif %}
{% endfor %}

setup_nm_failure:
  test.fail_without_changes:
    - name: Failed to configure NetworkManager minion_mac={{ minion_mac }}
    - onfail:
      - setup_nm
