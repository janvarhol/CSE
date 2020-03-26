{% import_yaml "cr.yml" as mw_keys %}

show:
  test.configurable_test_state:
    - name: show
    - changes: False
    - result: True
    - comment: |
        {{ mw_keys['Charlesriver'] }}


{% set tasks = mw_keys.values %}

show_tasks:
  test.configurable_test_state:
    - name: show tasks
    - changes: False
    - result: True
    - comment: |
        {{ tasks }}
