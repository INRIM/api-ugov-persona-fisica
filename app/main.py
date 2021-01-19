import logging
import os
import string
import time
import uuid
from functools import lru_cache
import requests

from fastapi import FastAPI, Request, Header, HTTPException

from services import *
from models import *
from datetime import *
import time as time_
import config

logger = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": ":-)",
        "description": "API REST per l'integrazione con WSACPersonaFisica (SOAP) di U-GOV JP",
        "externalDocs": {
            "description": "UGOV WS DOCS",
            "url": "https://wiki.u-gov.it/confluence/pages/viewpage.action?pageId=79822895&src=contextnavpagetreemode",
        }
    },
    {
        "name": "base",
        "description": "API Base",
    },
]


@lru_cache()
def get_settings():
    return config.Settings()


app = FastAPI(
    title=get_settings().app_name,
    description=get_settings().app_desc,
    version=get_settings().app_version,
    openapi_tags=tags_metadata
)


def check_token_get_auth(token: str) -> UgovAuth:
    if not token:
        raise HTTPException(status_code=401, detail="Auth invalid")
    logger.info("check_token_get_auth")
    utils = UtilsForService()
    jwt_settings = get_settings()._jwt_settings
    data = utils.decode_token(token, jwt_settings)
    if "username" in data and "password" in data:
        auth = UgovAuth(username=data['username'], password=data['password'], base_url_ws=get_settings().base_url_ws)
        return auth
    else:
        logger.error("jwt string invalid")
        raise HTTPException(status_code=401, detail="Auth invalid")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = str(uuid.uuid4())
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time_.time()

    response = await call_next(request)

    process_time = (time_.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.get("/", tags=["base"])
async def service_status():
    """
    Ritorna lo stato del servizio
    """
    return {"status": "live"}


@app.post("/genera-token", tags=["base"])
async def genera_token(tokendata: Token):
    """
    Genera un token JWT
    """
    utils = UtilsForService()
    token_str = utils.create_token(tokendata.dict())

    return {"token": token_str}


# Aggiungi il codice qui

@app.get("/v1/persone", tags=["v1 persona"])
async def elenca_persone(
        cognome: Optional[str] = None,
        nome: Optional[str] = None,
        matricola: Optional[str] = None,
        authtoken: str = Header(None)
) -> dict:
    """
    Binding del servizio SOAP U-GOV [elencaPersone](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-elencaPersone)

    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    res = pf.lista_persone(
        {
            "cognome": cognome,
            "nome": nome,
            "matricola": matricola
        }
    )

    return res


@app.get("/v1/estrai-persona-base", tags=["v1 persona"])
async def estrai_persona_base(
        dataRiferimento: Optional[date] = None,
        client: Optional[str] = None,
        codAnagrafico: Optional[str] = None,
        codEsse3: Optional[str] = None,
        codEsterno: Optional[str] = None,
        codiceFiscale: Optional[str] = None,
        EMail: Optional[str] = None,
        erroreUtenzaDoppia: Optional[str] = None,
        idInterno: Optional[str] = None,
        matricola: Optional[str] = None,
        nome: Optional[str] = None,
        userAlias: Optional[str] = None,
        username: Optional[str] = None,
        authtoken: str = Header(None)
) -> dict:
    """
    Binding del servizio SOAP U-GOV [estraiPersonaBase](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-estraiPersonaBase)

    """
    auth = check_token_get_auth(authtoken)

    res = PersonaFisicaService(auth).estrai_persona_base(
        {
            "dataRiferimento": dataRiferimento,
            "client": client,
            "codAnagrafico": codAnagrafico,
            "codEsse3": codEsse3,
            "codEsterno": codEsterno,
            "codiceFiscale": codiceFiscale.upper() if codiceFiscale else None,
            "EMail": EMail,
            "erroreUtenzaDoppia": erroreUtenzaDoppia,
            "idInterno": idInterno,
            "matricola": matricola,
            "nome": nome,
            "userAlias": userAlias,
            "username": username
        }
    )

    return res


@app.get("/v1/estrai-persona", tags=["v1 persona"])
async def estrai_persona(
        dataRiferimento: date,
        client: Optional[str] = None,
        codAnagrafico: Optional[str] = None,
        codEsse3: Optional[str] = None,
        codEsterno: Optional[str] = None,
        codiceFiscale: Optional[str] = None,
        EMail: Optional[str] = None,
        erroreUtenzaDoppia: Optional[str] = None,
        idInterno: Optional[str] = None,
        matricola: Optional[str] = None,
        nome: Optional[str] = None,
        userAlias: Optional[str] = None,
        username: Optional[str] = None,
        authtoken: str = Header(None)
) -> dict:
    """
    Binding del servizio SOAP U-GOV [estraiPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-estraiPersona)

    """
    auth = check_token_get_auth(authtoken)

    res = PersonaFisicaService(auth).estrai_persona(
        {
            "dataRiferimento": dataRiferimento,
            "client": client,
            "codAnagrafico": codAnagrafico,
            "codEsse3": codEsse3,
            "codEsterno": codEsterno,
            "codiceFiscale": codiceFiscale.upper() if codiceFiscale else None,
            "EMail": EMail,
            "erroreUtenzaDoppia": erroreUtenzaDoppia,
            "idInterno": idInterno,
            "matricola": matricola,
            "nome": nome,
            "userAlias": userAlias,
            "username": username
        }
    )

    return res


@app.post(
    "/v1/persona", tags=["v1 persona"]
)
async def inserisci_persona(
        persona: Persona,
        authtoken: str = Header(None)
) -> dict:
    """
    Binding del servizio SOAP U-GOV [inserisciPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-inserisciPersona)
    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    data = {k: v for k, v in persona.dict().items() if v != ''}
    res = pf.inserisci_persona(data)

    return res


@app.put(
    "/v1/persona/{tipo_campo}/{valore}", tags=["v1 persona"]
)
async def modifica_persona(
        tipo_campo: TipoCampoRicerca,
        valore: str,
        persona: Persona,
        authtoken: str = Header(None)
) -> dict:
    """
    Binding del servizio SOAP U-GOV [modificaPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-modificaPersona)
    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    data = {k: v for k, v in persona.dict().items() if v != ''}

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
            raise HTTPException(status_code=401, detail="IdIntenrno deve essere un numero")

        search = {
            "idInterno": int(valore)
        }
    elif tipo_campo.value == TipoCampoRicerca.username:
        search = {
            "username": valore
        }

    res = pf.modifica_persona(search, data)

    return res

# get persona/{ID}
