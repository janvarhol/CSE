{% set stage = pillar['stage'] %}

grain_patching_status:
  grains.present:
    - name: patching
    - value:
      - status: 'done'
      - comment: {{ stage }}
    - force: true
