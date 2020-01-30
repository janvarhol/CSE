{% set luks_assessment = salt['luks_test_data.test_data']() %}

# Checking if returned output has two arguments
# 0: Boolean
# 1: status
{% if luks_assessment | length >= 2 %}
{% if 'status' in luks_assessment[1] %}
{% set encrypted_devices = luks_assessment[1]['status']['encrypted devices'] %}
{% for encrypted_device in encrypted_devices %}
show-{{ encrypted_device }}:
  test.configurable_test_state:
    - name: Show info - {{ encrypted_device }}
    - changes: False
    - result: True
    - comment: |
        {{ encrypted_device }}
{% endfor %}
{% endif%}
{% endif %}
