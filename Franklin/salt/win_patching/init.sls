{% import_yaml "win_patching/win_patching_rules.yaml" as win_patching_rules %}

{% for osfinger in win_patching_rules['rules'] %}
{% if osfinger.lower() == 'Red Hat Enterprise Linux Server-7'.lower() %}

show_info:
  test.configurable_test_state:
    - name: Show osfinger
    - changes: false
    - result: true
    - comment: {{ osfinger }}

# Get patches list
{% set patches = win_patching_rules['rules'][osfinger]['patches_order'] %}
show_info_2:
  test.configurable_test_state:
    - name: Show patches
    - changes: false
    - result: true
    - comment: {{ patches }}

{% endif %}
{% endfor %}
