# Update and sync modules
update_modules:
  module.run:
    - name: saltutil.sync_all
    - refresh: True
 
 
{% set luks_assessment = salt['lukscheck.get_disks_encrypted']() %}
 
# Checking if returned output has two arguments
# 0: Boolean
# 1: status
{% if luks_assessment | length >= 2 %}
{% if 'status' in luks_assessment[1] %}
{% set encrypted_devices = luks_assessment[1]['status']['encrypted devices'] %}
{% for device in encrypted_devices %}
 
show-encrypted-device{{ device }}:
  test.configurable_test_state:
    - name: Show encryped device - {{ device }}
    - changes: False
    - result: True
    - comment: |
        {{ device }}
 
# This will call the original function with the device
{% set real_device = device.replace('/','_') %}
 
show-real-device{{ real_device }}:
  test.configurable_test_state:
    - name: Show real device - {{ real_device }}
    - changes: False
    - result: True
    - comment: |
        {{ real_device }}
 
# Get the Pillar encryption key
{%    set encryption_key = salt['pillar.get']("luks:"+real_device+":encryption_key") %}
 
show-encrypted-key{{ device }}:
  test.configurable_test_state:
   - name: Show encrypted key  - {{ encryption_key }}
    - changes: False
    - result: True
    - comment: |
        {{ encryption_key }}
 
# Check if there is an encryption key from Pillar DATA
# There is a seperate state file that sets that Pillar DATA
{%    if encryption_key %}
 
test_luks_encryption_on_{{ device }}:
  luks.encrypted_with_key:
    - name: {{ device }}
    - key: {{ encryption_key }}
    - require:
      - update_modules
      # - sls: enc_compliance.gpg_prep
 
not_encrypted_with_key_{{ device }}:
  event.send:
    - name: ebay/compliance/luks/not_encrypted_with_key
    - onfail:
      - test_luks_encryption_on_{{ device }}
 
luks_compliant_{{ device }}:
  event.send:
    - name: ebay/compliance/luks/compliant
    - require:
      - test_luks_encryption_on_{{ device }}
 
{%    else -%}
 
  # There is no encryption key stored in pillar.
  # This only runs if test_check_for_encryption_key_check_pillar fails
 
request_new_key_from_master_for_{{ device }}:
  event.send:
    - name: ebay/compliance/luks/newkey
    - data:
        event: new_encryption_key
        device: {{ real_device }}
{#        # enc_key_b64: {{salt['hashutil.base64_encodestring'](enc_key_res['comment'])}} #}
 
 
test_there_is_no_key_for_encryption:
  test.configurable_test_state:
    - name: there_is_no_key_for_encryption
    - changes: True
    - result: False
    - comment: |
        There is no key for encryption on this machine. A message has been sent
        to the master requesting that a key be created. The master will re-run
        this state when the key is ready
 
# End of encrypt key check
{%    endif %}
 
{% endfor %}
 
{% endif%}
{% endif %}
