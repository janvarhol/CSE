{% set name = salt['pillar.get']('name', 'Unknown User') %}
{% set description = salt['pillar.get']('description', 'Unknown Client') %}
{% set mac = salt['pillar.get']('mac', None) %}
{% set minion_id = salt['pillar.get']('minion_id', None) %}
{% set num_fails = salt['pillar.get']('num_fails', 0) | int %}
{% set reason = salt['pillar.get']('reason', None) %}
{% set email = "{someemail@example.com}" %}

send_email:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: '{{ email }}'
    - subject: Linux Access Management Portal - Device Not Compliant
    - template: salt://master/files/email/test_email.txt
    - context:
        name: {{ name }}
        description: {{ description }}
        mac: {{ mac }}
        minion_id: {{ minion_id }}
        num_fails: {{ num_fails }}
        reason: {{ reason }}
