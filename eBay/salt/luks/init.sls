{% set disks_encrypted = salt['luks.get_disks_encrypted']() %}

{% if disks_encrypted == True %}
success_check:
  test.succeed_without_changes:
    - name: "All disks encrypted"
{% else %}
fail_check:
  test.fail_without_changes:
    - name: "Not All disks encrypted"
{% endif %}
