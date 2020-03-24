#salt-run state.orch orch.url_request2 pillar='{"minion_id": "minion2"}'
{% set minion_id = salt['pillar.get']('minion_id', '') %}
{% set minion_data = salt['url_request.get_minion_data'](minion_id=minion_id) %}


{% if minion_data is mapping and minion_data | length and 'minion_id' in minion_data %}
show_info:
  test.configurable_test_state:
    - name: show info
    - changes: false
    - result: true
    - comment: |
        lenght: {{ minion_data|length }}
        dict: {{ minion_data }}

show_minion_data:
  test.configurable_test_state:
    - name: show minion data
    - changes: false
    - result: true
    - comment: |
        origin: {{ minion_data['info'] }}

{% else %}
show_error_not_valid_minion_data:
  test.configurable_test_state:
    - name: not valid minion data
    - changes: false
    - result: false
    - comment: not valid minion data
    - failhard: true
{% endif %}

do_more_stuff:
  test.configurable_test_state:
    - name: do more stuff
    - changes: false
    - result: true
    - comment: |
        Doing more stuff
