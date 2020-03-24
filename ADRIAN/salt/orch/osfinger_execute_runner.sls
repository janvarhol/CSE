# This state does
# salt-run salt.execute 'ebay' 'grains.item' arg=['osfinger']

{% set minion_id = 'MY_MINION-1' %}
{% set minion_osfinger = salt.saltutil.runner(name='salt.execute', arg=[minion_id, 'grains.item'], kwarg={'arg': ['osfinger']}) %}

show_info:
  test.configurable_test_state:
    - name: show info
    - changes: False
    - result: True
    - comment: |
        {{ minion_osfinger[minion_id]['osfinger'] }}
