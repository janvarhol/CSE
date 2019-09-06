show_basic_pillar_git_SixGroup:
  test.configurable_test_state:
    - name: github - SixGroup - show basic pillar information
    - changes: false
    - result: true
    - comment: {{ pillar['CSE'] }} - {{ pillar['PS'] }}
