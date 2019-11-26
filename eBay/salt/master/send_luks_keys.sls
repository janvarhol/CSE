{% set email = salt['pillar.get']('email') %}
{% set name = salt['pillar.get']('name') %}
{% set mac = salt['pillar.get']('mac') %}
{% set minion_id = salt['pillar.get']('minion_id') %}
{% set keys = salt['pillar.get']('keys') %}
{% set description = salt['pillar.get']('description') %}
{% set email_admin = salt['pillar.get']('email_admin') %}

send_email_user:
  module.run:
    - name: mime.send_msg
    - profile: ebay-smtp
    - recipient: "{{ email }}"
    - subject: Linux Access Management Portal - LUKS Keys Contained
    - template: salt://master/files/email/send_luks_keys.txt
    - context:
        name: {{ name }}
        minion_id: {{ minion_id }}
        description: {{ description }}
        keys: {{ keys|yaml }}
        mac: {{ mac }}
        email_admin: {{ email_admin }}

