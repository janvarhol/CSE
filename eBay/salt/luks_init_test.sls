{#{% set luks_assessment = salt['luks_test_data.test_data']() %}#}
{% set luks_assessment = salt['luks_check.get_disks_encrypted']() %}

# Checking if returned output has two arguments
# 0: Boolean
# 1: status
{% if luks_assessment | length >= 2 %}
{% if 'status' in luks_assessment[1] %}
{% set encrypted_devices = luks_assessment[1]['status']['encrypted devices'] %}

{% for encrypted_device in encrypted_devices %}
{% set real_device = encrypted_device.replace('/','_') %}
show-{{ encrypted_device }}:
  test.configurable_test_state:
    - name: Show info - {{ encrypted_device }}
    - changes: False
    - result: True
    - comment: |
        {{ encrypted_device }}  -- {{ real_device }}

# WORK THIS PART
{# {%    set encryption_key = salt['pillar.get']("luks:"+real_device+":encryption_key") %} #}
{% set encryption_key = 'ee2953ac-f696-478f-83bd-7ba71715ba68' %}
{# {%    if encryption_key %} #}

test_luks_encryption_on_{{ encrypted_device }}:
  luks.encrypted_with_key:
    - name: {{ encrypted_device }}
    - key: {{ encryption_key }}
#   - require:
#     - update_modules


{% endfor %}
{% endif%}
{% endif %}
