#############################################
# This state is meant to be run on the master
#############################################
#{# for x in ['lamp/files/certs', 'cert/minions', 'encryption'] #}
{% for folder in ['cert/files', 'cert/minions', 'encryption'] %}
prep_folders_{{folder}}:
  file.directory:
    - name: {{pillar['saltlocal_path']}}/salt/{{folder}}
    - user: root
    - group: root
    - makedirs: true
    - require_in:
      - deploy_config
{% endfor %}

file_roots_outside_git:
  file.managed:
    - name: /etc/salt/master.d/file_roots.conf
    - source: salt://master/files/file_roots.conf
    - template: jinja

deploy_config:
  file.managed:
    - name: /etc/salt/master.d/luks_ext_pillar.conf
    - source: salt://master/files/luks_ext_pillar.conf
    - template: jinja

restart_master:
  module.run:
    - name: service.restart
    - m_name: salt-master
    - watch:
      - deploy_config
      - file_roots_outside_git
