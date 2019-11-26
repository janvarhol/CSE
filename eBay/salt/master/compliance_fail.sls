{% set reason = salt['pillar.get']('reason', None) %}
{% set email = salt['pillar.get']('email', None) %}
{% set minion_id = salt['pillar.get']('minion_id', None) %}
{% set num_fails = salt['pillar.get']('num_fails', 0) | int %}
{% set description = salt['pillar.get']('description', 'Unknown Client') %}
{% set max_fails = salt['pillar.get']('max_fails', 0) | int %}
{% set mac = salt['pillar.get']('mac', None) %}
{% set name = salt['pillar.get']('name', 'Unknown User') %}
{% set msg_admin = salt['pillar.get']('msg_admin', False) %}
{% set email_admin = salt['pillar.get']('email_admin', None) %}
{% set scan_date = salt.lampapi.get_last_update(minion_id) %}

{% if not reason %}
fail_reason:
  test.fail_without_changes:
    - name: Reason not defined via inline pillar
    - failhard: True
{% elif not email %}
fail_email:
  test.fail_without_changes:
    - name: Email not defined via inline pillar
    - failhard: True
{% elif not minion_id %}
fail_minion:
  test.fail_without_changes:
    - name: Minion not defined via inline pillar
    - failhard: True
{% endif %}

update_db:
  module.run:
    - name: lampapi.post_result
    - minion_id: {{ minion_id }}
    - success: False
    - failure_reason: {{ reason }}

{% if salt['date_compare.is_today'](scan_date) %}
{% if msg_admin %}
# Send a message to the admin as well as the user. This may indicate an issue
# that admins needs to be aware of and fix.
send_email_admin:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: {{ email_admin }}
    - subject: Linux Access Management Portal - Device Not Compliant
    - template: salt://master/files/email/device_not_compliant_admin.txt
    - context:
        name: {{ name }}
        description: {{ description }}
        mac: {{ mac }}
        minion_id: {{ minion_id }}
        num_fails: {{ num_fails }}
        reason: {{ reason }}
        email_admin: {{ email_admin }}

send_email_user:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: "{{ email }}"
    - subject: Linux Access Management Portal - Device Not Compliant
    - template: salt://master/files/email/device_not_compliant_notified.txt
    - context:
        name: {{ name }}
        description: {{ description }}
        mac: {{ mac }}
        minion_id: {{ minion_id }}
        num_fails: {{ num_fails }}
        reason: {{ reason }}
        email_admin: {{ email_admin }}

{% else %}
# Send email to the user. This is an issue the user must resolve.
send_email_user:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: "{{ email }}"
    - subject: Linux Access Management Portal - Device Not Compliant
    - template: salt://master/files/email/device_not_compliant.txt
    - context:
        name: {{ name }}
        description: {{ description }}
        mac: {{ mac }}
        minion_id: {{ minion_id }}
        num_fails: {{ num_fails }}
        reason: {{ reason }}
        email_admin: {{ email_admin }}

{% endif %}

{% if num_fails >= max_fails %}

sleep_1:
  module.run:
    - name: test.sleep
    - length: 2
remove_mac_from_ise:
  module.run:
    - name: ise.delete_mac
    - mac: {{ mac }}

{#
{% salt.log.debug('device_removal::: device %s for %s not compliant: %s', mac, name, reason) %}
#}

send_remove_email:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: {{ email }}
    - subject: Linux Access Management Portal - Network Access Revoked
    - template: salt://master/files/email/access_revoked.txt
    - context:
        name: {{ name }}
        description: {{ description }}
        mac: {{ mac }}
        minion_id: {{ minion_id }}
        num_fails: {{ num_fails }}
        reason: {{ reason }}
        email_admin: {{ email_admin }}

{% endif %}
{% endif %}

##
# Need to return a failure so we can stop execution in Orchestration state that calls this
fail_hard:
  test.configurable_test_state:
    - name: Always fail
    - changes: False
    - result: False
