# Orchestration state to whitelistt a minion in ISE
{% set mac = salt['pillar.get']('mac', None) %}
##

whitelist_mac:
  salt.function:
    - name: ise.assign_group
    - tgt: {{ salt['pillar.get']('master_id')}} 
    - arg:
      - eBay_Linux_Nonprovisioned
      - {{ mac }}

whitelist_mac_failure:
  test.fail_without_changes:
    - name: "'{{ mac }}' was not able to be whitelistedns"
    - failhard: True
    - onfail:
      - salt: whitelist_mac
