import logging
import os
import requests
import string
import time
import time as time_
import uuid
from datetime import *
from fastapi import FastAPI, Request, Header, HTTPException, Depends
from functools import lru_cache

from models import *
from services import *
from settings import get_settings

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

responses = {
    401: {
        "description": "Token non valido",
        "content": {"application/json": {"example": {"detail": "Auth invalid"}}}},
    422: {
        "description": "Dati richiesta non corretti",
        "content": {"application/json": {"example": {"detail": "err messsage"}}}}
}

app = FastAPI(
    title=get_settings().app_name,
    description=get_settings().app_desc,
    version="1.1.0",
    openapi_tags=tags_metadata,
    openapi_url="/persona-fisica/openapi.json",
    docs_url="/persona-fisica/docs",
    redoc_url="/persona-fisica/redoc",
)


def check_token_get_auth(token: str) -> Auth:
    if not token:
        raise HTTPException(status_code=401, detail="Auth invalid")
    logger.info("check_token_get_auth")

    utils = UtilsForService()
    jwt_settings = get_settings().jwt_settings
    print(jwt_settings)
    data = utils.decode_token(token, jwt_settings)

    if "username" in data and "password" in data:
        auth = Auth(username=data['username'], password=data['password'],
                    base_url_ws=get_settings().base_url_ws)
        return auth
    else:
        logger.error("jwt string invalid")
        raise HTTPException(status_code=401, detail="Auth invalid")


def check_response_data(res_data: dict) -> dict:
    if res_data.get("status") and res_data.get("status") == "error":
        raise HTTPException(status_code=422, detail=res_data['message'])
    else:
        return res_data


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = str(uuid.uuid4())
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time_.time()

    response = await call_next(request)
    process_time = (time_.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.get("/persona-fisica/", tags=["base"])
async def service_status():
    """
    Ritorna lo stato del servizio
    """
    return {"status": "live"}


@app.post(
    "/persona-fisica/genera-token",
    responses=responses,
    tags=["base"])
async def genera_token(tokendata: Token):
    """
    Genera un token JWT
    """
    utils = UtilsForService()
    token_str = utils.create_token(tokendata.dict())

    return {"token": token_str}


# Aggiungi il codice qui

@app.get(
    "/persona-fisica/v1/persone",
    response_model=ListPersonaSearch,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    response_model_exclude_defaults=True,
    responses=responses,
    tags=["v1 persona"])
async def elenca_persone(
        cognome: Optional[str] = None,
        nome: Optional[str] = None,
        matricola: Optional[str] = None,
        authtoken: str = Header(None)
):
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

    return check_response_data(res)


@app.get(
    "/persona-fisica/v1/estrai-persona-base",
    response_model=PersonaFisicaResp,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    response_model_exclude_defaults=True,
    responses=responses,
    tags=["v1 persona"])
async def estrai_persona_base(
        persona: PersonaSearch = Depends(),
        authtoken: str = Header(None)
):
    """
    Binding del servizio SOAP U-GOV [estraiPersonaBase](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-estraiPersonaBase)

    """
    auth = check_token_get_auth(authtoken)
    res = PersonaFisicaService(auth).estrai_persona_base(persona)
    logger.info(f"Response data --> {res}")

    return check_response_data(res)


@app.get(
    "/persona-fisica/v1/estrai-persona",
    response_model=PersonaFisicaResp,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    response_model_exclude_defaults=True,
    responses=responses,
    tags=["v1 persona"])
async def estrai_persona(
        ricereca_persona: PersonaSearch = Depends(),
        authtoken: str = Header(None)
):
    """
    Binding del servizio SOAP U-GOV [estraiPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-estraiPersona)

    """
    auth = check_token_get_auth(authtoken)

    res = PersonaFisicaService(auth).estrai_persona(ricereca_persona)

    return check_response_data(res)


@app.post(
    "/persona-fisica/v1/persona",
    response_model=InserisciPersonaResponse,
    responses=responses,
    tags=["v1 persona"]
)
async def inserisci_persona(
        persona: Persona,
        authtoken: str = Header(None)
):
    """
    Binding del servizio SOAP U-GOV [inserisciPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-inserisciPersona)
    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    res = pf.inserisci_persona(persona)

    return check_response_data(res)


@app.put(
    "/persona-fisica/v1/persona",
    response_model=BaseSuccessResponse,
    responses=responses,
    tags=["v1 persona"]
)
async def modifica_persona(
        persona: Persona,
        ricereca_persona: PersonaSearch = Depends(),
        authtoken: str = Header(None)
) -> dict:
    """
    Binding del servizio SOAP U-GOV [modificaPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-modificaPersona)
    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    res = pf.modifica_persona(ricereca_persona, persona)

    return check_response_data(res)


# get persona/{ID}

# elencaGruppiPersona;
@app.get(
    "/persona-fisica/v1/gruppi-parsona",
    response_model=UtenteGruppiReponse,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    response_model_exclude_defaults=True,
    responses=responses,
    tags=["v1 gruppi persona"])
async def elenca_gruppi_persona(
        ricerca_persona: PersonaSearch = Depends(),
        authtoken: str = Header(None)
):
    """
    Binding del servizio SOAP U-GOV [elencaGruppiPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-elencaGruppiPersona)

    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    res = pf.elenca_gruppi_persona(ricerca_persona)

    return check_response_data(res)


# inserisciPersonaInGruppi;
@app.post(
    "/persona-fisica/v1/gruppi-parsona",
    response_model=BaseSuccessResponse,
    responses=responses,
    tags=["v1 gruppi persona"])
async def inserisci_persona_in_gruppi(
        gruppi_persona: ListaGruppiPersona,
        ricerca_persona: PersonaSearch = Depends(),
        authtoken: str = Header(None)
):
    """
    Binding del servizio SOAP U-GOV [elencaGruppiPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-inserisciPersonaInGruppi)

    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    res = pf.inserisci_persona_in_gruppi(ricerca_persona, gruppi_persona)

    return check_response_data(res)


# eliminaPersonaDaGruppi.
@app.delete(
    "/persona-fisica/v1/gruppi-parsona",
    response_model=BaseSuccessResponse,
    responses=responses,
    tags=["v1 gruppi persona"])
async def elimina_persona_da_gruppi(
        gruppi_persona: ListaGruppiPersona,
        ricerca_persona: PersonaSearch = Depends(),
        authtoken: str = Header(None)
):
    """
    Binding del servizio SOAP U-GOV [elencaGruppiPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-eliminaPersonaDaGruppi)

    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    res = pf.elimina_persona_da_gruppi(ricerca_persona, gruppi_persona)

    return check_response_data(res)


# elencaProfiliPersona;
@app.get(
    "/persona-fisica/v1/profili-parsona",
    response_model=UtenteProfiliResponse,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    response_model_exclude_defaults=True,
    responses=responses,
    tags=["v1 profili persona"])
async def elenca_profili_persona(
        ricerca_persona: PersonaSearch = Depends(),
        authtoken: str = Header(None)
):
    """
    Binding del servizio SOAP U-GOV [elencaGruppiPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-elencaProfiliPersona)

    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    res = pf.elenca_profili_persona(ricerca_persona)

    return check_response_data(res)


# inserisciProfiliInGruppi;
@app.post(
    "/persona-fisica/v1/profili-parsona",
    response_model=BaseSuccessResponse,
    responses=responses,
    tags=["v1 profili persona"])
async def inserisci_persona_in_profili(
        profili_persona: ListaProfiliPersona,
        ricerca_persona: PersonaSearch = Depends(),
        authtoken: str = Header(None)
):
    """
    Binding del servizio SOAP U-GOV [elencaGruppiPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-inserisciPersonaInProfili)

    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    res = pf.inserisci_persona_in_profili(ricerca_persona, profili_persona)

    return check_response_data(res)


# eliminaProfiliDaGruppi.
@app.delete(
    "/persona-fisica/v1/profili-parsona",
    response_model=BaseSuccessResponse,
    responses=responses,
    tags=["v1 profili persona"])
async def elimina_persona_da_profili(
        profili_persona: ListaProfiliPersona,
        ricerca_persona: PersonaSearch = Depends(),
        authtoken: str = Header(None)
):
    """
    Binding del servizio SOAP U-GOV [elencaGruppiPersona](https://wiki.u-gov.it/confluence/pages/releaseview.action?pageId=79822895#WSACPersonaFisica(SOAP)-eliminaPersonaDaProfili)

    """
    auth = check_token_get_auth(authtoken)
    pf = PersonaFisicaService(auth)
    res = pf.elimina_persona_da_profili(ricerca_persona, profili_persona)

    return check_response_data(res)
