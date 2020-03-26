# salt/mwmodern/

{% import_yaml "cr.yml" as mw_keys %}

#{% set hosts = salt['pillar.get']('nodes', 'PILLAR MINION NOT FOUND!') %}

{% set prev_func_name = [] %}

{% set tasks = mw_keys.values() %}

{% for activities in tasks[0] %}

{% set job = activities.values() %}

{% for item in job[0] %}

{% for key,val in item.items() %}
{{ key }}:
  salt.runner:
    - name: state.orchestrate
    - mods: {{ val[1]['FILE_PATH'] }}
    - pillar:
        nodes: [{{ val[0]['NAME'] }}]
    {% if prev_func_name|length > 1 %}
    - require:
      - salt: {{ prev_func_name[-1] }}
    {% endif %}

{% if val[2]['REBOOT_WAIT_FLAG'] %}

wait_for_reboot_{{ val[0]['NAME'] }}:
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - {{ val[0]['NAME'] }}
    - timeout: 300
    - require:
      - salt: {{ key }}

{% endif %}


{% if val[3]['REBOOT_REQ_FLAG'] %}

reboot_{{ val[0]['NAME'] }}:
  salt.function:
    - name: cmd.run_bg
    - arg:
      - 'salt-call system.reboot'
    - tgt: {{ val[0]['NAME'] }}
    - require:
      - salt: {{ key }}

wait_for_after_file_rename_reboot_{{ val[0]['NAME'] }}:
  salt.wait_for_event:
    - name: salt/minion/*/start
    - id_list:
      - {{ val[0]['NAME'] }}
    - timeout: 300
    - require:
      - salt: reboot_{{ val[0]['NAME'] }}

{% endif %}

{% do prev_func_name.append(key) %}



{% endfor %}

{% endfor %}

{% endfor %}
