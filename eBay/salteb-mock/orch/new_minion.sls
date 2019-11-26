# Orchestration state to add accept new minion key, notify peer master of new key
{% set minion_id = salt['pillar.get']('minion_id', None) %}
{% set minion_data = salt['lampapi.get_minion'](minion_id) %}

{% if minion_data.minion_id != minion_id %}

Unknown minion_id:
  test.fail_without_changes:
    - name: "'{{ minion_id }}' does not match any known minions"
    - failhard: True

{% else %}

minion_add:
  salt.wheel:
    - name: key.accept
    - match: {{ minion_id }}

pause:
  salt.runner:
    - name: test.sleep
    - s_time: 5
    - require:
      - salt: minion_add
  
deploy_schedule:
  salt.state:
    - tgt: {{ minion_id }}
    - sls:
      - minion.schedule
    - require:
      - salt: minion_add

deploy_modules:
  salt.function:
    - name: saltutil.sync_modules
    - tgt: {{ minion_id }}
    - require:
      - salt: minion_add

compliance_scan:
  salt.runner:
    - name: state.orch
    - mods:
      - orch.compliance
    - pillar:
        minion_id: {{ minion_id }}

# enable_presence:
#  salt.state:
#    - tgt: {{ minion_id }}
#    - sls:
#      - presence
#    - require:
#      - salt: minion_add

{% endif %}
