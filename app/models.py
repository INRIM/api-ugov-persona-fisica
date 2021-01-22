from enum import Enum
from pydantic import BaseModel, Field, PrivateAttr
from typing import List, Optional, Generic, TypeVar
import base64
from datetime import date, datetime, time, timedelta

from pydantic.generics import GenericModel
import logging

logger = logging.getLogger(__name__)


class UgovAuth(BaseModel):
    username: str
    password: str
    base_url_ws: str
    _token: str = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        token = f"{self.username}:{self.password}"
        bytemsg = base64.b64encode(token.encode('utf-8'))
        tokenb64 = str(bytemsg, "utf-8")
        self._token = f"Basic {tokenb64}"


class Token(BaseModel):
    username: str
    password: str
    secret: str
    alg: str


ItemT = TypeVar('ItemT')


class BaseSuccessResponse(BaseModel):
    Success: str = "done"


class BaseErrorResponse(BaseModel):
    status: str = "error"
    message: str


class ListModel(GenericModel, Generic[ItemT]):
    items: List[ItemT]
    length: int


class DataModel(GenericModel, Generic[ItemT]):
    data: ItemT


class TipoCampoRicerca(str, Enum):
    codice_fiscale = "Codice Fiscale"
    matricola = "Matricola"
    username = "Nome Utente (uid)"
    id_interno = "idInterno"


class Utente(BaseModel):
    dataFineUtente: Optional[datetime] = None
    dataInizioUtente: Optional[datetime] = None
    descrUtente: Optional[str] = ""
    distNameLDap: Optional[str] = ""
    EMail: Optional[str] = ""
    indirizzoUtente: Optional[str] = ""
    telefonoUtente1: Optional[str] = ""
    telefonoUtente2: Optional[str] = ""
    username: Optional[str] = ""
    utenteBloccato: Optional[bool] = None
    utenteLDAP: Optional[bool] = None
    utentePwdScaduta: Optional[bool] = None


# Gruppi

class GruppoPersona(BaseModel):
    nomeGruppo: str = ""
    descrGruppo: Optional[str] = ""
    sistema: Optional[bool] = False


class ListaGruppiPersona(BaseModel):
    elencoGruppi: List[GruppoPersona]


class UtenteGruppi(BaseModel):
    listaGruppi: Optional[List[GruppoPersona]] = None
    utente: Utente


class UtenteGruppiReponse(BaseModel):
    gruppiUtente: UtenteGruppi


# Profili

class ProfiliPersona(BaseModel):
    codiceProfilo: str = ""
    nomeProfilo: Optional[str] = ""
    descrProfilo: Optional[str] = ""
    tipoProfilo: Optional[str] = ""


class ListaProfiliPersona(BaseModel):
    elencoProfili: List[ProfiliPersona]


class UtenteProfili(BaseModel):
    listaProfili: Optional[List[ProfiliPersona]] = None
    utente: Utente


class UtenteProfiliResponse(BaseModel):
    profiliUtente: UtenteProfili


# Persona
class Persona(BaseModel):
    nome: str = ""
    cognome: str = ""
    codNazioneNascita: str = ""
    genere: str = ""
    dataNascita: str = ""
    codComuneNascita: str = ""
    codiceFiscale: Optional[str] = ""
    matricola: Optional[str] = ""
    username: Optional[str] = ""
    EMail: Optional[str] = ""
    distNameLDap: Optional[str] = ""
    telUfficio: Optional[str] = ""


class InserisciPersonaResponse(BaseModel):
    idInterno: Optional[int] = None


class ListPersona(BaseModel):
    Persone: List[Persona]


class PersonaSearch(BaseModel):
    client: Optional[str] = ""
    codAnagrafico: Optional[str] = ""
    codEsse3: Optional[str] = ""
    codEsterno: Optional[str] = ""
    codiceFiscale: Optional[str] = ""
    cognome: Optional[str] = ""
    dataRiferimento: Optional[date] = None
    EMail: Optional[str] = ""
    erroreUtenzaDoppia: Optional[str] = ""
    idInterno: Optional[int] = None
    matricola: Optional[str] = ""
    nome: Optional[str] = ""
    userAlias: Optional[str] = ""
    username: Optional[str] = ""

    def __init__(self, **data):
        super().__init__(**data)
        self.codiceFiscale = self.codiceFiscale.upper()


class ListPersonaSearch(BaseModel):
    PersonaFisica: Optional[List[PersonaSearch]] = None


class PersonaFisica(BaseModel):
    addettoAntiFumo: Optional[bool] = None
    addettoPrevIncendi: Optional[bool] = None
    addettoPrimoSoccorso: Optional[bool] = None
    appartieneOrdineReligioso: Optional[bool] = None
    badge: Optional[str] = ""
    caoStranieroDomFiscale: Optional[str] = ""
    capDomFiscale: Optional[str] = ""
    capDomicilio: Optional[str] = ""
    capResidenza: Optional[str] = ""
    capStranieraDomicilio: Optional[str] = ""
    capStranieraResidenza: Optional[str] = ""
    casellaPostaleDomicilio: Optional[str] = ""
    categoriaProtettaAssunzione: Optional[bool] = None
    cdCia: Optional[str] = ""
    cdEsse3: Optional[str] = ""
    cellPersonale: Optional[str] = ""
    cellUfficio: Optional[str] = ""
    cittaStranieraNascita: Optional[str] = ""
    civicoDomFiscale: Optional[str] = ""
    civicoDomicilio: Optional[str] = ""
    civicoResidenza: Optional[str] = ""
    codASLDomicilio: Optional[str] = ""
    codASLResidenza: Optional[str] = ""
    codAnagrafico: Optional[str] = ""
    codCategoriaProtetta: Optional[str] = ""
    codComuneDomFiscale: Optional[str] = ""
    codComuneDomicilio: Optional[str] = ""
    codComuneNascita: Optional[str] = ""
    codComuneResidenza: Optional[str] = ""
    codEsterno: Optional[str] = ""
    codNazioneCittadinanza: Optional[str] = ""
    codOnorifico: Optional[str] = ""
    codSdi: Optional[str] = ""
    codTipoDocIdentita: Optional[str] = ""
    codiceEsternoRU: Optional[str] = ""
    codiceFiscale: Optional[str] = ""
    codiceFiscaleEstero: Optional[str] = ""
    cognome: Optional[str] = ""
    cognomeAcquisito: Optional[str] = ""
    cpFlag: Optional[bool] = None
    cpNumeroCasella: Optional[str] = ""
    cpUfficio: Optional[str] = ""
    dataAssunzionePubblica: Optional[datetime] = None
    dataCategoriaProtetta: Optional[datetime] = None
    dataDocIdentitaRilascio: Optional[datetime] = None
    dataFineDomFiscale: Optional[datetime] = None
    dataFineDomicilio: Optional[datetime] = None
    dataFineResidenza: Optional[datetime] = None
    dataFineUtente: Optional[datetime] = None
    dataInizioDomFiscale: Optional[datetime] = None
    dataInizioDomicilio: Optional[datetime] = None
    dataInizioResidenza: Optional[datetime] = None
    dataInizioUtente: Optional[datetime] = None
    dataNascita: Optional[datetime] = None
    descrCittaStranieraDomFiscale: Optional[str] = ""
    descrCittaStranieraDomicilio: Optional[str] = ""
    descrCittaStranieraResidenza: Optional[str] = ""
    descrEnteRilascioDocIdentita: Optional[str] = ""
    descrUtente: Optional[str] = ""
    distNameLDap: Optional[str] = ""
    domicilioPressoTerzi: Optional[str] = ""
    EMail: Optional[str] = ""
    edificioDomFiscale: Optional[str] = ""
    edificioDomicilio: Optional[str] = ""
    edificioResidenza: Optional[str] = ""
    esoneroObbligoResidenza: Optional[bool] = None
    fax: Optional[str] = ""
    fornitoreCritico: Optional[bool] = None
    frazioneDomFiscale: Optional[str] = ""
    frazioneDomicilio: Optional[str] = ""
    frazioneResidenza: Optional[str] = ""
    genere: Optional[str] = ""
    idInterno: Optional[int] = None
    indirizzoDomFiscale: Optional[str] = ""
    indirizzoDomicilio: Optional[str] = ""
    indirizzoResidenza: Optional[str] = ""
    indirizzoUtente: Optional[str] = ""
    matricola: Optional[str] = ""
    nome: Optional[str] = ""
    note: Optional[str] = ""
    noteRisorsaUmana: Optional[str] = ""
    numeroDocIdentita: Optional[str] = ""
    PEC: Optional[str] = ""
    partitaIva: Optional[str] = ""
    partitaIvaEstero: Optional[str] = ""
    percCategoriaProtetta: Optional[int] = None
    postaElettronicaPrivata: Optional[str] = ""
    postaElettronicaUfficio: Optional[str] = ""
    psCodQuestura: Optional[str] = ""
    psDataFine: Optional[datetime] = None
    psDataInizio: Optional[datetime] = None
    psDataPres: Optional[datetime] = None
    psMotivo: Optional[str] = ""
    psNote: Optional[str] = ""
    psNumero: Optional[str] = ""
    psStato: Optional[str] = ""
    quartiereDomFiscale: Optional[str] = ""
    quartiereDomicilio: Optional[str] = ""
    quartiereResidenza: Optional[str] = ""
    le: Optional[bool] = None
    rifUfficio: Optional[str] = ""
    secondoNome: Optional[str] = ""
    skype: Optional[str] = ""
    statoCivile: Optional[str] = ""
    telCasa: Optional[str] = ""
    telDomicilio: Optional[str] = ""
    telUfficio: Optional[str] = ""
    telefonoUtente1: Optional[str] = ""
    telefonoUtente2: Optional[str] = ""
    urlSitoWeb: Optional[str] = ""
    urlcv: Optional[str] = ""
    userAlias: Optional[str] = ""
    username: Optional[str] = ""
    utenteBloccato: Optional[int] = None
    utenteLDAP: Optional[int] = None
    utentePwdScaduta: Optional[int] = None


class PersonaFisicaResp(BaseModel):
    personaFisica: PersonaFisica
