show_basic_pillar_git_YoungLiving:
  test.configurable_test_state:
    - name: github - Franklin - show basic pillar information
    - changes: false
    - result: true
    - comment: {{ pillar['CSE'] }} - {{ pillar['PS'] }}
