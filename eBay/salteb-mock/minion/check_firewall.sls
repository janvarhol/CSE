{% if salt['service.status']('firewalld') %}
{% set status = 'firewalld' %}
{% elif salt['service.status']('ufw') %}
{% set status = 'ufw' %}
{% else %}
{% set status = 'iptables' %}
{% endif %}

firewall_in_use:
  test.succeed_without_changes:
    - name: {{ status }}
