import os


ovh_token_data = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "name": os.environ["OVH_USER_LOGIN"],
                    "domain": {
                        "id": "default"
                    },
                    "password": os.environ["OVH_USER_PWD"]
                }
            }
        },
        "scope": {
            "project": {
                "name": os.environ["OVH_TENANT_NAME"],
                "domain": {
                    "id": "default"
                }
            }
        }
    }
}