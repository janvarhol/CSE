{% import_yaml "orch/staged_patching.yaml" as patching_flow %}


# RUN PRE-FLIGHT CHECKS
# Check all the required pillar items
# STOP if required pillar not found
test_check_pillar:
  test.check_pillar:
    - present:
      - minion
    - failhard: true
# Receive and give default value to pillar if requested pillar is not present
{% set minion = salt['pillar.get']('minion', 'PILLAR MINION NOT FOUND!') %}
test_show_pillar_values:
  test.configurable_test_state:
    - name: Show Pillar values
    - changes: false
    - result: true
    - comment: |
        PILLAR VALUES
        1-minion: {{ minion }}



# Prepare system for patching
# failhard if pre checks fails
# 1 - stop apps and services
# TBD

# 2 - unmount remote file systems
# TBD

# 3 - disconnect users
# TBD

# 4 - PPS: PRE-PATCH STAGE COMPLETE send event to start patching process
send_reboot_for_patching_event:
  salt.function:
    - name: event.send
    - tgt: {{ minion }}
    - arg:
      - 'patching/start'
    - kwarg:
        stage: PPS
        order: patching-start


# 5 - (restart by event.send -> reactor)
# wait_for_reboot)

wait_for_reboot-PPS:
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - {{ minion }}
    - timeout: 120
    - require:
      - salt: send_reboot_for_patching_event

# Loop thru stages
{% for stage in patching_flow.stages.keys() %}

# Loop thru patches list in each stage and execute patch
{% for patch in patching_flow['stages'][stage]['patches'] %}
{{ stage }}-{{ patch }}-{{ minion }}:
  salt.state:
    - tgt: {{ minion }}
    - sls:
      - {{ patch }}
{% endfor %}  # PATCHES LOOP END


# Check if stage requires reboot
{% if patching_flow['stages'][stage]['reboot_required'] %}
reboot_required-{{ stage }}:
  test.configurable_test_state:
    - name: show data
    - comment: Reboot required - {{ stage }}
    - result: true
    - changes: false

grain_reboot_required-{{ stage }}:
  salt.state:
    - tgt: {{ minion }}
    - sls:
      - patching.patch-set_reboot_required_grain
    - pillar:
        stage: {{ stage }}
        minion: {{ minion }}

reboot_minion-{{ stage }}:
  salt.function:
    - name: cmd.run_bg
    - arg:
      - 'salt-call system.reboot'
    - tgt: {{ minion }}

wait_for_reboot-{{ stage }}:
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - {{ minion }}
    - timeout: 120
    - require:
      - salt: reboot_minion-{{ stage }}

grain_reboot_required_after_reboot-{{ stage }}:
  salt.state:
    - tgt: {{ minion }}
    - sls:
      - patching.patch-set_reboot_required_after_reboot
    - pillar:
        stage: {{ stage }}
        minion: {{ minion }}
    - require:
      - salt: wait_for_reboot-{{ stage }}

{% endif %}

{% endfor %} # STAGES LOOP END



# POST PATCHING READINESS
#1 Mount remote filesystes
#TBD

#2 - enable and start apps and services
#TBD


grain_reboot_patching-complete:
  salt.state:
    - tgt: {{ minion }}
    - sls:
      - patching.patch-set_patching_complete_grains
    - pillar:
        stage: 'PATCHING COMPLETE'
        minion: {{ minion }}
#    - require::
#      - some: POST_PATCHING_READINESS_CHECKS
