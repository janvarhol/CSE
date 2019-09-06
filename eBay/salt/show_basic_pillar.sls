show_basic_pillar_git_eBay:
  test.configurable_test_state:
    - name: github - eBay - show basic pillar information
    - changes: false
    - result: true
    - comment: {{ pillar['CSE'] }} - {{ pillar['PS'] }}
