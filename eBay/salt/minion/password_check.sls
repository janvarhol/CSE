{% set username = salt['pillar.get']('username', 'Unknown') %}
test_check-for-username_pillar:
  # keys to check existence(comma-separated): username
  # value types to check for(comma-separated): string
  test.check_pillar:
    - present:
      - username
    - failhard: True
#    - comment: Must suppy a 'username' via pillar
# Line removed to fix bug reported by Krunal 03/27/2019


{% set days = salt['pillar.get']('password_compliance_days', 90) %}
{% set info = salt['ebayshadow.info'](username) %}

{% if info.passwd.startswith("!") or info.passwd.startswith("*") %}
account_disabled:
  test.succeed_without_changes:
    - name: "'{{ username }}' password last changed is compliant - account LOCKED"
#{% elif info.passwd == '' %}
#missing_password:
#  test.fail_without_changes:
#    - name: "'{{ username }}' password has a NULL value and does not match compliance requirement"
{% elif info.sincelstchg > days %}
fail_check:
  test.fail_without_changes:
    - name: "'{{ username }}' password does not match compliance requirement of last changed in {{ days }} days - last changed {{ info.sincelstchg }} days"
{% else %}
success_check:
  test.succeed_without_changes:
    - name: "'{{ username }}' password last changed is compliant - last changed {{ info.sincelstchg }} days"
{% endif %}
