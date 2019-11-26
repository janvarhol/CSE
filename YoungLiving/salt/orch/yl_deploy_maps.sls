# If using pillar to define environYL
# test.check_pillar will stop immediately
# if environYL is not present in pillar
# Can be set in pillar files or
# passing pillar in CLI, like pillar pillar='{"environYL": "PROD123"}'
# CLI will show missing pillar information
check_pillar:
  test.check_pillar:
    - present:
      - environYL

# or
{% set environYL = salt['pillar.get']('environYL', None) %}
{% if environYL is not none %}

{% set instances_list = [] %}
{% set cloud_map_deploy = salt.saltutil.runner(name='cloud.map_run', arg=['/srv/salt/cloud/maps/lab_deploy-hasse-hasse1118-student1.map'], kwargs={'parallel': True}) %}

{% for instance in cloud_map_deploy %}
{% do instances_list.append(instance) %}
{% endfor %}

{% if instances_list|count > 0 %}
{% for instance in instances_list %}
do_something_with_{{ instance }}:
  test.configurable_test_state:
    - name: Execute some action on {{ instance }}
    - changes: False
    - result: True
    - comment: Configuring {{ instance }}

test_connected_{{ instance }}:
  salt.function:
    - tgt: {{ instance }}
    - name: test.ping
{% endfor %}
{% endif %}
{% endif %}
