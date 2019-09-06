# Code to check pillar values are received
# Check all the required pillar items
test_check_pillar:
  test.check_pillar:
    - present:
      - sender_id
      - minion_id
#    - failhard: true

# Receive and give default value to pillar if requested pillar is not present
{% set sender_id = salt['pillar.get']('sender_id','PILLAR NOT FOUND!') %}
{% set minion_id = salt['pillar.get']('minion_id', 'PILLAR NOT FOUND!') %}
test_show_pillar_values:
  test.configurable_test_state:
    - name: Show Pillar values
    - changes: false
    - result: true
    - comment: |
        PILLAR VALUES
        1-sender_id: {{ sender_id }}
        2-minion_id: {{ minion_id }}
# OPTIONAL
#    - require:
#      - test: test_check_pillar # Will not execute this state if test_check_pillar fails
# SAVE PILLAR VALUES TO FILE
test_save_pillar_2file:
  file.managed:
    - name: /tmp/pillar_info.txt
    - contents: |
        PILLAR VALUES
        1-sender_id: {{ sender_id }}
        2-minion_id: {{ minion_id }} 
