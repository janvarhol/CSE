{% set minion_macs = salt['url_request.request_get']() %}

{% if minion_macs|is_iter and minion_macs|length %}
show_info:
  test.configurable_test_state:
    - name: show info
    - changes: false
    - result: true
    - comment: |
        lenght: {{ minion_macs|length }}
        dict: {{ minion_macs|tojson }}

show_minion_data:
  test.configurable_test_state:
    - name: show minion data
    - changes: false
    - result: true
    - comment: |
        origin: {{ minion_macs['origin'] }}

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
