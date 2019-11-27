show_basic_pillar_git_Schlumberger:
  test.configurable_test_state:
    - name: github - Schlumberger - show basic pillar information
    - changes: false
    - result: true
    - comment: {{ pillar['CSE'] }} - {{ pillar['PS'] }}
