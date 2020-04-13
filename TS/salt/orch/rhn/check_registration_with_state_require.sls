# Orchestration using custom mod: _modules/rhn_mock.py
{% set minion = pillar['minion'] %}

check-pillar-minion-is-present:
  test.check_pillar:
    - present:
        - minion
    - failhard: True

# Check registration
# Module returns True/False
check_minion_rhn_registration:
  salt.runner:
    - name: rhn_mock.hammer_info
    - minion_id: {{ minion }}

rhn_registration_is_True:
  test.succeed_without_changes:
    - name: {{ minion }} is registered on RHN
    - require:
      - salt: check_minion_rhn_registration
# NOTE: require works as expected given the use of
# __context__['retcode'] = 1
# in runner module

# MOCK EXAMPLE
register_minion:
  test.configurable_test_state:
    - name: Registering {{ minion }} on RHN
    - comment: Registering {{ minion }} on RHN
    - changes: False
    - result: True
    - onfail:
      - salt: check_minion_rhn_registration