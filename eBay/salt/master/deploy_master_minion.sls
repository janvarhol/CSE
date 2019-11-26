#############################################
# This state is meant to be run on the master
#############################################
deploy_config:
  file.managed:
    - name: /etc/salt/minion.d/smtp.conf
    - source: salt://master/files/smtp.conf

restart_minion:
  module.run:
    - name: service.restart
    - m_name: salt-minion
    - require:
      - file: deploy_config
