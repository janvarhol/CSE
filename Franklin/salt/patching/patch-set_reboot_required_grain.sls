{% set stage = pillar['stage'] %}
{% set minion = pillar['minion'] %}

grain_patching_status:
  grains.present:
    - name: patching
    - value:
      - status: 'in progress'
      - comment: {{ stage }}
    - force: true

grain_reboot_required:
  grains.present:
    - name: patching:{{ stage }}:reboot
    - value:
      - reboot_required: 'yes'
      - comment: Pending reboot required by patching {{ stage }}
    - force: true
