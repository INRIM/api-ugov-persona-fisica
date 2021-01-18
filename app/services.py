from jose import JWTError, jwt

from requests import Response

from models import *
from zeep import Client
import logging
import xmltodict

logger = logging.getLogger(__name__)


class UtilsForService:

    def _finditem(self, obj, key):
        if key in obj: return obj[key]
        for k, v in obj.items():
            if isinstance(v, dict):
                item = self._finditem(v, key)
                if item is not None:
                    return item

    def parseResponse(self, response: Response, objectName: str, faultString: str) -> dict:
        if response.status_code == 200:
            base = xmltodict.parse(response.content)
            ret = self._finditem(base, objectName)
            if not type(ret) is dict:
                ret = {objectName: ret}
        else:
            base = xmltodict.parse(response.content)
            dat = self._finditem(base, faultString)
            ret = {'satus': 'error', "message": dat}
        return ret

    def extract_jwt(self, token: str, jwt_settings: dict) -> dict:
        pass

    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        secret_key = data.pop('secret')
        algorithm = data.pop('alg')
        if "expire_minute" in data:
            if data['expire_minute']:
                data['expire'] = datetime.datetime.utcnow() + data['expire_minute']
            else:
                data.pop('expire_minute')
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    def create_int_token(self, data: dict, jwt_settings: dict) -> str:
        to_encode = {**data, **jwt_settings}
        return self.create_token(to_encode)

    def decode_token(self, token: str, jwt_settings: dict) -> dict:
        return jwt.decode(token, jwt_settings.get('secret'), algorithms=[jwt_settings.get('alg')])


class PersonaFisicaService(object):

    def __init__(self, auth: UgovAuth):
        self.wsdlurl = f'{auth.base_url_ws}/ws-ac/ws/private/PersonaFisica?wsdl'
        logger.info("PersonaFisicaService Init")
        self.auth = auth
        self.utils = UtilsForService()

    def lista_persone(self, data: dict) -> dict:
        client = Client(self.wsdlurl)
        with client.settings(raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.elencaPersone(data)
            djson = self.utils.parseResponse(response, "PersonaFisica", "faultstring")
            return djson

    def inserisci_persona(self, data: dict) -> dict:
        client = Client(self.wsdlurl)
        with client.settings(strict=False, raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.inserisciPersona(personaFisica=data)
            djson = self.utils.parseResponse(response, "idInterno", "faultstring")
            return djson

    def estrai_persona_base(self, data: dict) -> dict:
        client = Client(self.wsdlurl)
        with client.settings(raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.estraiPersonaBase(data)
            djson = self.utils.parseResponse(response, "personaFisica", "faultstring")
            return djson

    def estrai_persona(self, data: dict) -> dict:
        client = Client(self.wsdlurl)
        with client.settings(raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.estraiPersona(dtoRicerca=data)
            djson = self.utils.parseResponse(response, "personaFisica", "faultstring")
            return djson
