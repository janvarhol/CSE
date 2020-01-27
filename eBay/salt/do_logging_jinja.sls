{% set minion = 'my_minion' %}
{% set name = 'my_device' %}
{% set mac = '0a:2d:bc:90:8a:64' %}
{% set reason = 'Time to leave the network' %}



# OK
{% do salt.log.info('--->> minion: {}, name: {}, mac: {}, reason: {}'.format(minion,name,mac,reason)) %}
{% do salt.log.info('--->> DIFFERENT FORMAT minion: %s, name: %s, mac: %s, reason: %s' % (minion, name, mac ,reason)) %}


my-custom-combo:
  test.configurable_test_state:
    - name: Do some logging
    - changes: False
    - result: True
    - comment: Logging test
