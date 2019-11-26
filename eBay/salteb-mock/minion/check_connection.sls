test_wired-ebay-corp_connection:
# AM: STATE MODIFIED FOR TESTING
  test.configurable_test_state:
    - name: SIMULATED test_wired-ebay-corp_connection
    - changes: False
    - result: True
{#
  test.configurable_test_state:
    - result: {{ salt['nmcli.active']('wired-ebay-corp')}}
    - changes: false
#}
