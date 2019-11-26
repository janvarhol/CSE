compliance_fail:
  test.configurable_test_state:
    - name: SIMULATED COMPLIANCE_FAIL
    - changes: False
    - result: True

##
# Need to return a failure so we can stop execution in Orchestration state that calls this
fail_hard:
  test.configurable_test_state:
    - name: Always fail
    - changes: False
    - result: False


# AM: WHOLE STATE ACTUAL CONTENT REMOVED FOR TESTING
