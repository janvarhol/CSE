{% import_yaml "win_patching/test2.yaml" as win_patching_rules %}

{% for osfinger in win_patching_rules['rules'] %}
{% if osfinger.lower() == grains['osfinger'].lower() %}

show_info:
  test.configurable_test_state:
    - name: Show osfinger
    - changes: false
    - result: true
    - comment: Patching {{ osfinger }}

{% set patches_order = win_patching_rules['rules'][osfinger]['patches_order'] %}

# Download patches
{% for patches in patches_order %}
{% set patches_index = loop.index %}
{% for patch in patches %}
download_patches-{{ patches_index }}-{{ patch }}:
  test.configurable_test_state:
    - name: download {{ patch }}
    - changes: false
    - result: true
    - comment: |
        {{ patches[patch]['repo_link'] }}
{% endfor %}
{% endfor %}


# Install patches
{% for patches in patches_order %}
{% set patches_index = loop.index %}
{% for patch in patches %}
install_patches-{{ patches_index }}-{{ patch }}:
  test.configurable_test_state:
    - name: install {{ patch }}
    - changes: false
    - result: true
    - comment: |
        {{ patches[patch]['exec_cmd'] }}
{% endfor %}
{% endfor %}


{% else %}
show_not_applicable:
  test.configurable_test_state:
    - name: Not Applicable
    - changes: false
    - result: false
    - comment: This system is not applicable
{% endif %}
{% endfor %}
