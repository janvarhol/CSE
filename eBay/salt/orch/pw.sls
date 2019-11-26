test_minion_id_check_pillar:
  test.check_pillar:
    - present:
      - minion_id
      - master_id
    - failhard: True
    - comment: Must have a 'minion_id' and 'master_id' passed as a pillar

{% set master = salt['pillar.get']('master_id') %}
{% set minion_id = salt['pillar.get']('minion_id') %}
{% set minion_data = salt['lampapi.get_minion'](minion_id) %}

{% if minion_data.include_scan %}
password_check:
  salt.state:
    - tgt: {{ minion_id }}
    - sls:
        - minion.password_check
    - pillar:
        username: root

password_check_fail:
  salt.state:
    - tgt: {{ master }}
    - sls:
      - master.compliance_fail
    - pillar:
        minion_id: {{ minion_id }}
        reason: password check failure for local root account
        email: '{{ minion_data.email }}'
    - failhard: True
    - onfail:
      - password_check
{% else %}
do_not_run:
  test.succeed_without_changes:
    - name: {{ minion_id }} not included in scans {{ minion_data.include_scan }}
{% endif %}
{#
#}
