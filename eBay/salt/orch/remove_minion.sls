##
# Orch state to remove wire-ebay-corp connection, /etc/salt/pki, remove salt-minion

test_minion_id_check_pillar:
  test.check_pillar:
    - present:
      - minion_id

{% set minion_id = salt['pillar.get']('minion_id', None) %}

remove_minion_stuff:
  salt.state:
    - tgt: {{ minion_id }}
    - sls:
      - minion.remove_minion

pause_now:
  salt.runner:
    - name: test.sleep
    - s_time: 5

remove_key:
  salt.wheel:
    - name: key.delete
    - match: {{ minion_id }}
    - require:
      - salt: remove_minion_stuff

# TODO
# send email to qualys team notification that minion key is longer needed
# remove key from ise
