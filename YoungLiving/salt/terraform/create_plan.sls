# /srv/salt/terraform/create_plan.sls
{% set instance_name = salt['pillar.get']('instance_name', None) %}

create_plan_file:
  file.managed:
    - name: /root/terraform/plans/aws_deploy_instance.tf
    - source: salt://terraform/aws_deploy_instance.tf-template
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - defaults:
        instance_name: {{ instance_name }}
        
