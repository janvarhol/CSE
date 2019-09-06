show_basic_pillar_git_YoungLiving:
  test.configurable_test_state:
    - name: github - YoungLiving - show basic pillar information
    - changes: false
    - result: true
    - comment: {{ pillar['CSE'] }} - {{ pillar['PS'] }}
