{% set minion = salt['pillar.get']('minion', 'NO_MINION') %}
{% set minion_ip = salt['pillar.get']('minion_ip', 'NO_MINION_IP') %}
append_new_system-{{ minion }}:
  file.append:
    - name: /etc/salt/roster
    - source: salt://updatesalt/roster_template.yaml
    - template: jinja
    - context:
        minion_ip: {{ minion_ip }}
        minion: {{ minion }}