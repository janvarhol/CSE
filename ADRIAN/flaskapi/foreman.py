from flask import Flask, json, request

minion_data = [
{
    "minion_id": "tsystems",
    "subscription_facet_attributes":
        { "activation_keys":
                {
                    "id": 34,
                    "name": "tc - rhel - ot_unix - activation - key - ux"
                },
          "installed_products":
                {
                    "arch": "x86_64",
                    "product":
                        {
                            "productId": 111,
                            "productName": "RedHat 7 DevOps Bundle",
                            "version": "7"
                        }
                }
        },
    "autoheal": True,
},
{
    "minion_id": "ip-172-31-0-4.us-east-2.compute.internal",
    "subscription_facet_attributes":
        { "activation_keys":
                {
                    "id": 99,
                    "name": "tc - Solaris - ot_unix - activation - key - ux"
                },
          "installed_products":
                {
                    "arch": "ABC",
                    "product":
                        {
                            "productId": 777,
                            "productName": "Solaris XYZ",
                            "version": "7"
                        }
                }
        },
    "autoheal": False,
}
]

api = Flask(__name__)


# Endpoint to report minion_data
# Expects argument minion_id
# Example:
#   curl -X GET http://172.31.26.239:8080/minion_data?minion_id=minion1
@api.route('/minion_data', methods=['GET'])
def get_minion_data():
  api.logger.info('/minion_data GET call arg minion_id: %s', request.args.get('minion_id', ''))
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