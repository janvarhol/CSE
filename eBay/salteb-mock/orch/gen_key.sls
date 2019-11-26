{% set master = salt.pillar.get('master_id') %}

gen_key_for_minion:
  salt.state:
    - tgt: {{ master }}
    - sls:
      - luks.render_keyfile

    - pillar:
        device: {{ pillar.get('device') }}
        minion_id: {{ pillar.get('minion_id') }}

