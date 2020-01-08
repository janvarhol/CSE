{% set minion_data = salt['url_request.request_get']() %}
{# {% set minion_data = salt['url_request.request_put']('abcd1') %} #}

# If minion_data is dictionary, not empty and key 'origin' in dictionary
{% if minion_data is mapping and minion_data | length and 'origin' in minion_data %}
show_info:
  test.configurable_test_state:
    - name: show info
    - changes: false
    - result: true
    - comment: |
        lenght: {{ minion_data|length }}
        dict: {{ minion_data|tojson }}

show_minion_data:
  test.configurable_test_state:
    - name: show minion data
    - changes: false
    - result: true
    - comment: |
        origin: {{ minion_data['origin'] }}

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
