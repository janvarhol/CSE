import json
import sys


if len(sys.argv) > 1:
    minion = sys.argv[1]
    hammer_output = {
                        minion: {
                                    "Subscription Information": {
                                                                    "UUID": "392b8ebb-d145-41df-aaad-ed169ef01d08",
                                                                    "Last Checkin": "2020-04-08 09:44:39 UTC",
                                                                    "Service Level": "",
                                                                    "Release Version": "7.7",
                                                                    "Autoheal": True,
                                                                    "Registered To": "tgm1r627.gw.ux.tc.corp",
                                                                    "Registered At": "2020-04-08 09:44:29 UTC",
                                                                    "Registered by Activation Keys": {
                                                                                                        "1": {
                                                                                                                "Name": "tc-rhel-ot_unix-activation-key-ux",
                                                                                                                "Id": 34
                                                                                                            }
                                                                                                    }
                                                                }
                                }
    }

    print("RHN Satellite Hammer information for system: %s" % minion)
    print(json.dumps(hammer_output[minion], indent=4))
else:
    raise TypeError("Missing argument minion_id")
