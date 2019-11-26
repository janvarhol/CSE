#############################################
# This state is meant to be run on the master
#############################################

deploy_config:
  file.managed:
    - name: /etc/salt/master.d/reactor.conf
    - source: salt://master/files/reactor.conf

restart_master:
  module.run:
    - name: service.restart
    - m_name: salt-master
    - require:
      - file: deploy_config
