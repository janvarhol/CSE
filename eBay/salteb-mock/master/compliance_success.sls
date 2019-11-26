# AM: STATE MODIFIED FOR TESTING
notify_lamp_api_of_success:
  test.configurable_test_state:
    - name: SIMULATED lampapi.post_result
    - changes: False
    - result: True
    #- result: False
