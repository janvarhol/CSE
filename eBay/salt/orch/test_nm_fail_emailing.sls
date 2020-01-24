# Orchestration state to simulate compliance orchestration and emailing behavior for nm_fail

{% set minion_id = 'ebay' %}
{% set minion_data = {'email': 'amalaguti78@gmail.com', 'name': 'adrian m', 'description': 'doing some testing', 'num_fails': 4, 'macs': '0a:2d:bc:90:8a:64'} %}
{% set master = 'ebay' %}

update_success:
  test.fail_without_changes

manage_nm:
  test.succeed_without_changes:
    - require:
      - test: update_success
{#
show:
  test.configurable_test_state:
    - name: info
    - changes: false
    - result: true
    - comment: |
        {{ minion_data }}

#}

manage_nm_fail:
  salt.state:
    - tgt: {{ master }}
    - concurrent: True
    - sls:
      - master.nm_fail2
    - pillar:
        minion_id: {{ minion_id }}
        reason: Network Configuration Failure
        email: {{ minion_data.email }}
        name: {{ minion_data.name }}
        description: {{ minion_data.description }}
        num_fails: {{ minion_data.num_fails }}
        # NOTE: CHECK IF MAX FAILS IS SET IN PROD!! I HAD TO ADD IT MANUALLY HERE
        max_fails: 7
        # do not use this mac in prod
        mac: {{ minion_data.macs }}
    - failhard: True
    - onfail:
      - manage_nm
