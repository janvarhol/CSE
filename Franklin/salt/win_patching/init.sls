{% import_yaml "win_patching/win_patching_rules.yaml" as win_patching_rules %}

{% for osfinger in win_patching_rules['rules'] %}
{% if osfinger.lower() == 'Red Hat Enterprise Linux Server-7'.lower() %}

show_info:
  test.configurable_test_state:
    - name: Show osfinger
    - changes: false
    - result: true
    - comment: {{ osfinger }}


