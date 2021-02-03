from fastapi import HTTPException
from jose import JWTError, jwt

from requests import Response

from models import *
from zeep import Client
import logging
import xmltodict
import re

logger = logging.getLogger(__name__)


class UtilsForService:

    def _finditem(self, obj, key):
        if key in obj: return obj[key]
        for k, v in obj.items():
            if isinstance(v, dict):
                item = self._finditem(v, key)
                if item is not None:
                    return item

    def log_req_resp(self, req_resp: object):
        logger.info("------")
        logger.info("------")
        logger.info("--LOG RESP---")
        logger.info("..................................")
        logger.info(req_resp)
        logger.info("------")
        logger.info("------")

    def parseResponse(self, response: Response, object_name: str, fault_rtring: str,
                      sub_object_name: list = [], log_resp=False) -> dict:
        if log_resp:
            self.log_req_resp(response.content)
        if response.status_code == 200:
            base = xmltodict.parse(response.content)
            if sub_object_name:
                ret = {object_name: {}}
                for item in sub_object_name:
                    obj_item = self._finditem(base, item)
                    if "lista" in item and type(obj_item) is not list and obj_item:
                        obj_item = [obj_item]
                    ret[object_name][item] = obj_item
            else:
                ret = self._finditem(base, object_name)
            if not ret:
                ret = "done"
            if not type(ret) is dict:
                ret = {object_name: ret}
        else:
            base = xmltodict.parse(response.content)
            dat = self._finditem(base, fault_rtring)
            ret = {'status': 'error', "message": dat}
        return ret

    def extract_jwt(self, token: str, jwt_settings: dict) -> dict:
        pass

    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        secret_key = data.pop('secret')
        algorithm = data.pop('alg')
        if "expire_minute" in data:
            if data['expire_minute']:
                data['expire'] = datetime.utcnow() + data['expire_minute']
            else:
                data.pop('expire_minute')
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    def create_int_token(self, data: dict, jwt_settings: dict) -> str:
        to_encode = {**data, **jwt_settings}
        return self.create_token(to_encode)

    def decode_token(self, token: str, jwt_settings: dict) -> dict:
        return jwt.decode(token, jwt_settings.get('secret'), algorithms=[jwt_settings.get('alg')])

    def clean_body_data(self, data: BaseModel, log_req: bool = False) -> dict:
        req = {k: v for k, v in data.dict(exclude_unset=True).items() if not v == '' and v is not None}
        if log_req:
            self.log_req_resp(req)
        return req

    def make_search_base(self, tipo_campo: TipoCampoRicerca, valore: str) -> dict:

        if tipo_campo.value == TipoCampoRicerca.codice_fiscale:
            search = {
                "codiceFiscale": valore.upper()
            }
        elif tipo_campo.value == TipoCampoRicerca.matricola:
            search = {
                "matricola": valore
            }
        elif tipo_campo.value == TipoCampoRicerca.id_interno:
            try:
                x = int(valore)
            except Exception as e:
                return {"error": "IdIntenrno deve essere un numero"}

            search = {
                "idInterno": int(valore)
            }
        elif tipo_campo.value == TipoCampoRicerca.username:
            search = {
                "username": valore
            }
        else:
            return {"error": "dati non specificati"}

        return search


class PersonaFisicaService(object):

    def __init__(self, auth: UgovAuth):
        logger.info(f"-----------")
        logger.info(f"Init Service at {auth.base_url_ws}")
        logger.info(f"...")
        logger.info(f"complete url {auth.base_url_ws}/ws-ac/ws/private/PersonaFisica?wsdl")
        self.wsdlurl = f'{auth.base_url_ws}/ws-ac/ws/private/PersonaFisica?wsdl'
        self.auth = auth
        self.utils = UtilsForService()
        logger.info("PersonaFisicaService Init")

    def lista_persone(self, data: dict) -> dict:
        logger.info("prepare Client to start request")
        client = Client(self.wsdlurl)
        # data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        logger.info("Client create start request")
        with client.settings(raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.elencaPersone(data)
            djson = self.utils.parseResponse(response, "PersonaFisica", "faultstring", [])
            if djson.get('PersonaFisica') and not type(djson.get('PersonaFisica')) is list:
                dat = djson['PersonaFisica']
                djson['PersonaFisica'] = []
                if not dat == 'done':
                    djson['PersonaFisica'].append(dat)
            logger.info(djson)
            return djson

    def inserisci_persona(self, data: Persona) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(strict=False, raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.inserisciPersona(personaFisica=data)
            djson = self.utils.parseResponse(response, "idInterno", "faultstring")
            return djson

    def estrai_persona_base(self, data: PersonaSearch) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.estraiPersonaBase(data)
            djson = self.utils.parseResponse(response, "personaFisica", "faultstring")
            return djson

    def estrai_persona(self, data: PersonaSearch) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.estraiPersona(dtoRicerca=data)
            djson = self.utils.parseResponse(response, "personaFisica", "faultstring")
            return djson

    def modifica_persona(self, search_data: PersonaSearch, data: BaseModel) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        search_data = search_data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(strict=False, raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.modificaPersona(dtoRicerca=search_data, personaFisica=data)
            djson = self.utils.parseResponse(response, "Success", "faultstring")
            return djson

    def elenca_gruppi_persona(self, data: PersonaSearch) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(strict=False, raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.elencaGruppiPersona(data)
            djson = self.utils.parseResponse(
                response, "gruppiUtente", "faultstring", ['utente', 'listaGruppi'])
            return djson

    def inserisci_persona_in_gruppi(self, data: PersonaSearch, gruppi_persona: ListaGruppiPersona) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        gruppi_persona = gruppi_persona.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(strict=False, raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.inserisciPersonaInGruppi(data, gruppi_persona['elencoGruppi'])
            djson = self.utils.parseResponse(
                response, "Success", "faultstring", [])
            return djson

    def elimina_persona_da_gruppi(self, data: PersonaSearch, gruppi_persona: ListaGruppiPersona) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        gruppi_persona = gruppi_persona.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(strict=False, raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.eliminaPersonaDaGruppi(data, gruppi_persona['elencoGruppi'])
            djson = self.utils.parseResponse(
                response, "nomeGruppo", "faultstring", [])
            return djson

    def elenca_profili_persona(self, data: PersonaSearch) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(strict=False, raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.elencaProfiliPersona(data)
            djson = self.utils.parseResponse(
                response, "profiliUtente", "faultstring", ['utente', 'listaProfili'])
            return djson

    def inserisci_persona_in_profili(self, data: PersonaSearch, gruppi_persona: ListaProfiliPersona) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        gruppi_persona = gruppi_persona.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(strict=False, raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.inserisciPersonaInProfili(data, gruppi_persona['elencoProfili'])
            djson = self.utils.parseResponse(
                response, "nomeProfilo", "faultstring", [])
            return djson

    def elimina_persona_da_profili(self, data: PersonaSearch, gruppi_persona: ListaProfiliPersona) -> dict:
        client = Client(self.wsdlurl)
        data = data.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        gruppi_persona = gruppi_persona.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        with client.settings(strict=False, raw_response=True, extra_http_headers={'Authorization': self.auth._token}):
            response = client.service.eliminaPersonaDaProfili(data, gruppi_persona['elencoProfili'])
            djson = self.utils.parseResponse(
                response, "nomeProfilo", "faultstring", [])
            return djson
