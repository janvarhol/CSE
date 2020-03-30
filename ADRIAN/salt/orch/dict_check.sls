{% set stale_minions = {} %}


{# {% if stale_minions is not mapping or 'minion_id' not in stale_minions %} #}
{% if stale_minions | string | length == 0 %}
fail1:
  test.configurable_test_state:
    - name: fail1
    - changes: False
    - result: False
    - comment: |
        stale_minions is empty
        {{ stale_minions | string | length }}
    - failhard: True
  
fail2:
  test.configurable_test_state:
    - name: fail1
    - changes: False
    - result: False
    - comment: |
        test

{% elif 'minion_id' not in stale_minions %}
fail2:
  test.configurable_test_state:
    - name: fail2
    - changes: False
    - result: False
    - comment: |
        minion_id key not found in stale_minions dictionary
        {{ stale_minions | string }}
    - failhard: True

{% else %}
always-passes:
  test.succeed_without_changes:
    - name: Ok


{% endif %}
