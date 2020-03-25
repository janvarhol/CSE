# cat /opt/flask/flaskapi.py
from flask import Flask, json, request

test = [{"id": 1, "name": "SaltStack"}, {"id": 2, "name": "CSE"}]
services  = { "provider": "SaltStack",
                "Service": {
                    "CSE": "enabled",
                    "year": "2020" }
            }

minion_data = [ { "minion_id": "minion1",
                  "info": {
                    "model": "X",
                    "brand": "Y",
                    "year": 2018 }
                },
                { "minion_id": "minion2",
                  "info": {
                    "model": "A",
                    "brand": "Y",
                    "year": 2019 }
                }
              ]

api = Flask(__name__)

@api.route('/test', methods=['GET'])
def get_test():
  return json.dumps(test)

@api.route('/services', methods=['GET'])
def get_services():
  return json.dumps(services, indent=4)


# Endpoint to report minion_data
# Expects argument minion_id
# Example:
#   curl -X GET http://172.31.26.239:8080/minion_data?minion_id=minion1
@api.route('/minion_data', methods=['GET'])
def get_minion_data():
  api.logger.info('/minion_data GET call arg minion_id: %s',  request.args.get('minion_id', ''))
  minion_id = request.args.get('minion_id', '')


  if minion_id != '':
    for minion in minion_data:
      if minion['minion_id'] == minion_id:
        api.logger.info('minion_id: %s processed, full minion details: %s',  minion['minion_id'], minion)

        # Return minion data
        return json.dumps(minion, indent=4)

  # Return empty dict, no minion found
  return {}



@api.route('/posting', methods=['POST'])
def post_posting():
  if request.method == 'POST':
      json_data = request.get_json()
      return json.dumps({"method": "POST", "data": json_data}, indent=4), 201
  return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8080)
