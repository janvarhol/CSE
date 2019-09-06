show_basic_pillar_git:
  test.configurable_test_state:
    - name: github - show basic pillar information
    - changes: false
    - result: true
    - comment: {{ pillar['CSE'] }} - {{ pillar['PS'] }}
