# Show minion version
show_version:
  test.configurable_test_state:
    - name: show version
    - changes: false
    - result: true
    - comment: {{ grains['saltversion'] }}
