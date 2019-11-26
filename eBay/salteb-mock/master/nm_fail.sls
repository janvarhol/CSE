nm_fail:
  test.configurable_test_state:
    - name: SIMULATED NM_FAIL
    - changes: False
    - result: True

##
# Need to return a failure so we can stop execution in Orchestration state that calls this
fail_hard:
  test.configurable_test_state:
    - name: Always fail
    - changes: False
    - result: False









{# AM: STATE MODIFIED FOR TESTING
{% set reason = salt['pillar.get']('reason', None) %}
{% set email = salt['pillar.get']('email', None) %}
{% set minion_id = salt['pillar.get']('minion_id', None) %}
{% set num_fails = salt['pillar.get']('num_fails', 0) | int %}
{% set description = salt['pillar.get']('description', 'Unknown Client') %}
{% set max_fails = salt['pillar.get']('max_fails', 0) | int %}
{% set mac = salt['pillar.get']('mac', None) %}
{% set name = salt['pillar.get']('name', 'Unknown User') %}
{% set email_admin= salt['pillar.get']('email_admin', 'DL-eBay-OCIO-LAMP-Admins@ebay.com') %}

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

send_email:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: {{ email_admin }}
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

# Need to return a failure so we can stop execution in Orchestration state that calls this
fail_hard:
  test.configurable_test_state:
    - name: Always fail
    - changes: False
    - result: False
#}
