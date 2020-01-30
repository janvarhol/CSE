{% set disks_encrypted = salt['luks_check.get_disks_encrypted']() %}

{#
show:
  test.configurable_test_state:
    - name: show info
    - changes: False
    - result: True
    - comment: |
        {{ disks_encrypted }}
 #}      

# Modified to support new luks_check module
# position[0]: True/False
# position[1]: dictionary with luks status info
{% if disks_encrypted[0] == True %}
success_check:
  test.succeed_without_changes:
    - name: "All disks encrypted"
{% else %}
fail_check:
  test.fail_without_changes:
    - name: "Not All disks encrypted"
{% endif %}

