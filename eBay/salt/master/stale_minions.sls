###################################################################
# This state is meant to be run on the master to find stale minions
###################################################################
{% set email_admin = salt['pillar.get']('email_admin', None) %}
{#
{% set stale_minions = salt['lampapi.get_report']('all-minions') %}
#}
{% set stale_minions = salt['lampapi.get_report']('stale-minions') %}
{% for minion in stale_minions.minions %}
{% set stale_minion_data = salt['lampapi.get_minion'](minion.minion_id) %}
{% if stale_minion_data.include_scan == True %}

{% for mac in minion.macs %}
# extract last_update from the minion information. 
# Send a warning on pillar['fail_warnings'][n]
{#
test_{{ minion.minion_id }}_{{ mac }}:
  test.succeed_without_changes:
    - name: REMOVE {{ minion.minion_id }} MAC {{ mac }} from ISE
#}


remove_{{ mac }}:
  module.run:
    - name: ise.delete_mac
    - mac: {{ mac }}

remove_scan_{{ minion.minion_id }}:
  module.run:
    - name: lampapi.update_minion_scan
    - minion_id: {{ minion.minion_id }}
    - include_scan: False
    - require:
        - module: remove_{{ mac }}

alert_user_{{ mac }}:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: {{ stale_minion_data.email }}
    - subject: MAC removed from network
    - template: salt://master/files/email/stale_minion.txt
    - context:
        stale_minion_data: {{ stale_minion_data|json_encode_dict}}
        mac: {{ mac }}
        email_admin: {{ email_admin }}
    - require:
        - module: remove_scan_{{ minion.minion_id }}

alert_admin_{{ mac }}_on_delete:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: {{ email_admin }}
    - subject: MAC Deleted from ISE
    - template: salt://master/files/email/stale_minion.txt
    - context:
        stale_minion_data: {{ stale_minion_data|json_encode_dict}}
        mac: {{ mac }}
        email_admin: {{ email_admin }}
    - watch:
      - remove_{{mac}}

alert_admin_{{ mac }}_on_delete_fail:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: {{ email_admin }}
    - subject: Error deleting MAC from ISE
    - template: salt://master/files/email/error_deleting_mac.txt
    - context:
        stale_minion_data: {{ stale_minion_data|json_encode_dict}}
        mac: {{ mac }}
        email_admin: {{ email_admin }}
    - onfail:
      - module: remove_{{ mac }}

update_db_{{mac}}:
  module.run:
    - name: lampapi.post_result
    - minion_id: {{ minion.minion_id }}
    - success: True
    - failure_reason: "stale minion - no checks in 7 days" 

{% endfor %}
{% else %}
offline_{{ minion.minion_id }}:
  test.succeed_without_changes:
    - name: {{ minion.minion_id }} has already been removed
{% endif %}
{% endfor %}
