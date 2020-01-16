{% import_yaml "win_patching/win_patching_rules.yaml" as win_patching_rules %}

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
  file.managed:
    - name: 'C://{{ patches[patch]['filename'] }}'
    - source: {{ patches[patch]['repo_link'] }}
    #- skip_verify: true
{% endfor %}
{% endfor %}


# Install patches
{% for patches in patches_order %}
{% set patches_index = loop.index %}
{% for patch in patches %}
install_patches-{{ patches_index }}-{{ patch }}:
  cmd.run:
    - name: {{ patches[patch]['exec_cmd'] }}
    - success_retcodes: [3010]

{# Using module.run instead of state cmd.run
update:
  module.run:
    - name: cmd.run_bg
    - cmd: {{ patches[patch]['exec_cmd'] }}
    - output_loglevel: quiet
    - ignore_retcode: True
    - python_shell: True
    - timeout: 180
#}


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
