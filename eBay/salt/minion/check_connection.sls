test_wired-ebay-corp_connection:
  test.configurable_test_state:
    - result: {{ salt['nmcli.active']('wired-ebay-corp')}}
    - changes: false

