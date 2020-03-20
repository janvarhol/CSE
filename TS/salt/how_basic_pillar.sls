show_basic_pillar_git_ts:
  test.configurable_test_state:
    - name: github - TS - show basic pillar information
    - changes: false
    - result: true
    - comment: {{ pillar['CSE'] }} - {{ pillar['PS'] }}
