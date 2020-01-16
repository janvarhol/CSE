KB4534273:
  wusa.installed:
    - source: salt://windows10.0-kb4534273-x64_74bf76bc5a941bbbd0052caf5c3f956867e1de38.msu
# NOTE:
# Salt ouput shows error but
# return code 3010 means restart required
# Alternative: use cmd.run: 'wusa patch_file.msu' and - success_retcodes: [3010]

{% set restart_required = salt['system.get_pending_reboot']() %}

# restart system now
{% if restart_required %}
restart_minion:
  module.run:
    - name: cmd.run_bg
    - cmd: 'c:\\salt\\salt-call.bat --local system.reboot 0'

{% endif %}
