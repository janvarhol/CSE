{% set reason = salt['pillar.get']('reason', None) %}
{% set email = salt['pillar.get']('email', None) %}
{% set minion_id = salt['pillar.get']('minion_id', None) %}
{% set num_fails = salt['pillar.get']('num_fails', 0) | int %}
{% set description = salt['pillar.get']('description', 'Unknown Client') %}

# NOTE: CHECK IF MAX FAILS IS SET IN PROD!! I HAD TO ADD IT MANUALLY IN MY ORCH, was set to 0
{% set max_fails = salt['pillar.get']('max_fails', 7) | int %}

{% set mac = salt['pillar.get']('mac', None) %}
{% set name = salt['pillar.get']('name', 'Unknown User') %}

# Set default to False instead of None for email_admin
{% set email_admin= salt['pillar.get']('email_admin', False) %}

# Last scan/update
{% set last_notification = salt['pillar.get']('last_something', 'Wed Jan 20 10:52:08 UTC 2020') %}

{% set payload = {} %}
{% do payload.update({'reason': reason}) %}
{% do payload.update({'email': email}) %}
{% do payload.update({'minion_id': minion_id}) %}
{% do payload.update({'num_fails': num_fails}) %}
{% do payload.update({'description': description}) %}
{% do payload.update({'max_fails': max_fails}) %}
{% do payload.update({'mac': mac}) %}
{% do payload.update({'name': name}) %}
{% do payload.update({'email_admin': email_admin}) %}
{% do payload.update({'last_notification': last_notification}) %}
{% do payload.update({'email_profile': 'ebay-smtp'}) %}
{% do payload.update({'email_subject': 'Linux Access Management Portal - Network Configuration Issue'}) %}
{% do payload.update({'email_template': 'salt://master/files/email/network_config_issue.txt'}) %}

show payload:
  test.configurable_test_state:
    - name: nm_fail email payload
    - changes: false
    - result: true
    - comment: |
        {{ payload }}


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


{% if num_fails < max_fails %}
# Replace send email by NEW luks_email module
{% set email_sent = salt['compliance_email.send_email'](payload) %}

{% if email_sent %}
email_success:
  test.succeed_without_changes
{% else %}
email_fail:
  test.fail_without_changes
{% endif %}
{% endif %}




{# THE FOLLOWING WAS REPLACED BY NEW LUKS_EMAIL MODULE
send_email:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: {{ email }}
    - subject: Linux Access Management Portal - Network Configuration Issue
    - template: salt://master/files/email/network_config_issue.txt
    - context:
        name: {{ name }}
        description: {{ description }}
        mac: {{ mac }}
        minion_id: {{ minion_id }}
        num_fails: {{ num_fails }}
        reason: {{ reason }}
        email_admin: {{ email_admin }}
#}
