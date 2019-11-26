notify_lamp_api_of_success:
  module.run:
    - name: lampapi.post_result
    - minion_id: {{ pillar['minion_id'] }}
    - success: True
