# Orchestration using custom mod: _modules/rhn_mock.py
{% set minion = pillar['minion'] %}

check-pillar-minion-is-present:
  test.check_pillar:
    - present:
        - minion
    - failhard: True

{% set rhn_mock_runner = salt['saltutil.runner']('rhn_mock.hammer_info', arg=[minion]) %}

{% do salt.log.info('RHN MOCK: ORCHESTRATION: rhn_mock runner return check: %s' % rhn_mock_runner) %}

{% if rhn_mock_runner == True %}
minion_registered_true:
  test.succeed_without_changes
{% else %}
minion_registered_false:
  test.fail_without_changes
{% endif %}


# MOCK EXAMPLE, minion registragion if runner return is False
register_minion:
  test.configurable_test_state:
    - name: Registering {{ minion }} on RHN
    - comment: Registering {{ minion }} on RHN
    - changes: False
    - result: True
    - onfail:
      - test: minion_registered_false
