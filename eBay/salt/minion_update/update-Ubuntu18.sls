{% if grains['osfinger'].startswith('Ubuntu-18') %}

saltstack_repo_file:
  file.managed:
    - name: /etc/apt/sources.list.d/saltstack.list
    - source: salt://minion_update/Ubuntu18/saltstack.list

{% set add_repo_key = salt['pkg.add_repo_key']('salt://minion_update/Ubuntu18/SALTSTACK-GPG-KEY.pub') %}
{% set refresh_db = salt['pkg.refresh_db']() %}

update_minion:
  pkg.latest:
    - name: salt-minion
    - require:
      - file: saltstack_repo_file

{% else %}
bail_out:
  test.configurable_test_state:
    - name: Wrong platform
    - changes: False
    - result: False
    - comments: Check platform
{% endif %}
