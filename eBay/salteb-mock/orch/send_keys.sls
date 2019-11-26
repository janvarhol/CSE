##
# Orch state to send the user the luks keys for any encrypted volumes

test_minion_id_check_pillar:
  test.check_pillar:
    - present:
      - sender_id
      - minion_id

{% set minion_id = salt['pillar.get']('minion_id') %}
{% set sender_id = salt['pillar.get']('sender_id') %}

{% if sender_id in salt['pillar.get']('lamp:approved_key_senders') %}
## Only the lamp_minion can send the luks key sending event
{% set minion_macs = salt['lampapi.get_minion_macs'](minion_id) %}
{% set minion_data = salt.lampapi.get_minion(minion_id) %}
{% set master = salt.pillar.get('master_id') %}

# get keys and send to the user
# write email template

{% set keys_output = salt['saltutil.runner']('luks.keys', [minion_id])  %}

send_email_with_luks_keys:
  salt.state:
    - tgt: {{ master }}
    - concurrent: True
    - sls:
      - master.send_luks_keys
    - pillar:
        minion_id: {{ minion_id }}
        email: "{{ minion_data.email }}"
        description: {{ minion_data.description }}
        name: '{{ minion_data.name }}'
        keys: 
          {% for drive,v in keys_output[minion_id].items() %}
          - {{ drive }} => {{ v.encryption_key }}
          {% endfor %}
        mac: {{ minion_macs.macs[0] }}

{% endif %}
