{% import_yaml "orch/servers.yaml" as server %}

# This is a good way of testing data used by the state
# test.configurable_test_state let you manipulate state output and show data
# The for loop would generate duplicate state id by default
# The use of _{{ server }} in state ids inside for loop is to avoid duplicates
{% for server in server.name %}
show_{{ server }}:
  test.configurable_test_state:
    - name: show data
    - comment: {{ server }}
    - result: true
    - changes: false
 {% endfor %}

{% for server in server.name %}
patch_server_{{ server }}:
  salt.state:
    - tgt: {{ server }}
    - sls:
      - franklin.do_something
{% endfor %}
