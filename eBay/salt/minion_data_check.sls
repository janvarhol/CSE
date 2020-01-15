# cat test.sls
# Set some minion datastore
{% do salt['data.update']('a_string', 'SaltStack') %}
{% do salt['data.update']('a_list',  ['cse', 'consulting', 'support']) %}
{% do salt['data.update']('a_boolean_true', True) %}
{% do salt['data.update']('a_boolean_false', False) %}

# Load minion data store
{% set minion_data = salt['data.load']() %}


# Check if minion_data is defined and show info
{% if minion_data is defined %}
SHOW_DATA:
  test.configurable_test_state:
    - name: minion_data is DEFINED
    - changes: false
    - result: true
    - comment: |
        lenght: {{ minion_data|length }}
        data: {{ minion_data|tojson }}

# Check if minion_data is a dictionary, not empty (lenth > 0) and a key 'a_list' is present
{% if minion_data is mapping and minion_data | length and 'a_list' in minion_data %} #}
ALL_GOOD:
  test.configurable_test_state:
    - name: show info
    - changes: false
    - result: true
    - comment: |
        data: {{ minion_data|tojson }}
{% else %}
INVALID_MINION_DATA:
  test.configurable_test_state:
    - name: not valid minion data
    - changes: false
    - result: false
    - comment: not valid minion data
    - failhard: true
{% endif %}

{% else %}
UNDEFINED_MINION_DATA:
  test.configurable_test_state:
    - name: minion_data UNDEFINED
    - changes: false
    - result: false
    - comment: minion_data is not defined
    - failhard: true
{% endif %}
