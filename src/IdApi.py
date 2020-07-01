import json
from src.Signature import Signature
import requests


class IdApi:
    timestamp = 0
    sec_key = ""

    def __init__(self, partner_id, api_key, sid_server):
        if not partner_id or not api_key:
            raise Exception("partner_id or api_key cannot be null or empty")
        self.partner_id = partner_id
        self.api_key = api_key
        if sid_server in [0, 1]:
            sid_server_map = {
                0: "https://3eydmgh10d.execute-api.us-west-2.amazonaws.com/test",
                1: "https://la7am6gdm8.execute-api.us-west-2.amazonaws.com/prod",
            }
            self.url = sid_server_map[sid_server]
        else:
            self.url = sid_server

    def submit_job(self, partner_params, id_params):
        IdApi.validate_partner_params(partner_params)

        if not id_params:
            raise ValueError("Please ensure that you send through ID Information")

        self.validate_id_params(id_params)

        if partner_params.get("job_type") != 5:
            raise ValueError("Please ensure that you are setting your job_type to 5 to query ID Api")

        sec_key_object = self.__get_sec_key()
        payload = self.__configure_json(partner_params, id_params, sec_key_object["sec_key"],
                                        sec_key_object["timestamp"])
        response = self.__execute_http(payload)
        return response

    def __get_sec_key(self):
        sec_key_gen = Signature(self.partner_id, self.api_key)
        return sec_key_gen.generate_sec_key()

    def __configure_json(self, partner_params, id_params, sec_key, timestamp):
        payload = {
            "sec_key": sec_key,
            "timestamp": timestamp,
            "partner_id": self.partner_id,
            "partner_params": partner_params,
        }
        payload.update(id_params)
        return payload

    @staticmethod
    def validate_partner_params(partner_params):
        if not partner_params:
            raise ValueError("Please ensure that you send through partner params")

        if not partner_params["user_id"] or not partner_params["job_id"] or not partner_params["job_type"]:
            raise ValueError("Partner Parameter Arguments may not be null or empty")

        if not isinstance(partner_params["user_id"], str):
            raise ValueError("Please ensure user_id is a string")

        if not isinstance(partner_params["job_id"], str):
            raise ValueError("Please ensure job_id is a string")

        if not isinstance(partner_params["job_id"], str):
            raise ValueError("Please ensure job_id is a string")

        if not isinstance(partner_params["job_type"], int):
            raise ValueError("Please ensure job_id is a number")

    @staticmethod
    def validate_id_params(id_info_params):
        for field in ["country", "id_type", "id_number"]:
            if field in id_info_params:
                if id_info_params[field]:
                    continue
                else:
                    raise ValueError(field + " cannot be empty")
            else:
                raise ValueError(field + " cannot be empty")

    def __execute_http(self, payload):
        data = json.dumps(payload)
        resp = requests.post(
            url=self.url + "/id_verification",
            data=data,
            headers={
                "Accept": "application/json",
                "Accept-Language": "en_US",
                "Content-type": "application/json"
            })
        return resp
