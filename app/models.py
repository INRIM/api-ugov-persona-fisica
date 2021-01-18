from enum import Enum
from pydantic import BaseModel, Field, PrivateAttr
from typing import List, Optional, Generic, TypeVar
import base64
from datetime import date, datetime, time, timedelta

from pydantic.generics import GenericModel


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

ItemT = TypeVar('ItemT')


class ListModel(GenericModel, Generic[ItemT]):
    items: List[ItemT]
    length: int


class DataModel(GenericModel, Generic[ItemT]):
    data: ItemT


class Persona(BaseModel):
    nome: str
    cognome: str
    codNazioneNascita: str
    genere: str
    dataNascita: str
    codComuneNascita: str
    codiceFiscale: Optional[str] = None
    matricola: Optional[str] = None
    username: Optional[str] = None
    EMail: Optional[str] = None
    distNameLDap: Optional[str] = None
    telUfficio: Optional[str] = None


class ListPersona(BaseModel):
    Persone: List[Persona]


class Token(BaseModel):
    username: str
    password: str
    secret: str
    alg: str


class personaFisicaSearch(BaseModel):
    client: Optional[str] = None
    codAnagrafico: Optional[str] = None
    codEsse3: Optional[str] = None
    codEsterno: Optional[str] = None
    codiceFiscale: Optional[str] = None
    cognome: Optional[str] = None
    dataRiferimento: Optional[str] = None
    EMail: Optional[str] = None
    erroreUtenzaDoppia: Optional[str] = None
    idInterno: Optional[str] = None
    matricola: Optional[str] = None
    nome: Optional[str] = None
    userAlias: Optional[str] = None
    username: Optional[str] = None


class personaFisicaResponse(BaseModel):
    addettoAntiFumo: Optional[bool] = None
    addettoPrevIncendi: Optional[bool] = None
    addettoPrimoSoccorso: Optional[bool] = None
    appartieneOrdineReligioso: Optional[bool] = None
    badge: Optional[str] = None
    caoStranieroDomFiscale: Optional[str] = None
    capDomFiscale: Optional[str] = None
    capDomicilio: Optional[str] = None
    capResidenza: Optional[str] = None
    capStranieraDomicilio: Optional[str] = None
    capStranieraResidenza: Optional[str] = None
    casellaPostaleDomicilio: Optional[str] = None
    categoriaProtettaAssunzione: Optional[bool] = None
    cdCia: Optional[str] = None
    cdEsse3: Optional[str] = None
    cellPersonale: Optional[str] = None
    cellUfficio: Optional[str] = None
    cittaStranieraNascita: Optional[str] = None
    civicoDomFiscale: Optional[str] = None
    civicoDomicilio: Optional[str] = None
    civicoResidenza: Optional[str] = None
    codASLDomicilio: Optional[str] = None
    codASLResidenza: Optional[str] = None
    codAnagrafico: Optional[str] = None
    codCategoriaProtetta: Optional[str] = None
    codComuneDomFiscale: Optional[str] = None
    codComuneDomicilio: Optional[str] = None
    codComuneNascita: Optional[str] = None
    codComuneResidenza: Optional[str] = None
    codEsterno: Optional[str] = None
    codNazioneCittadinanza: Optional[str] = None
    codOnorifico: Optional[str] = None
    codSdi: Optional[str] = None
    codTipoDocIdentita: Optional[str] = None
    codiceEsternoRU: Optional[str] = None
    codiceFiscale: Optional[str] = None
    codiceFiscaleEstero: Optional[str] = None
    cognome: Optional[str] = None
    cognomeAcquisito: Optional[str] = None
    cpFlag: Optional[bool] = None
    cpNumeroCasella: Optional[str] = None
    cpUfficio: Optional[str] = None
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
    descrCittaStranieraDomFiscale: Optional[str] = None
    descrCittaStranieraDomicilio: Optional[str] = None
    descrCittaStranieraResidenza: Optional[str] = None
    descrEnteRilascioDocIdentita: Optional[str] = None
    descrUtente: Optional[str] = None
    distNameLDap: Optional[str] = None
    domicilioPressoTerzi: Optional[str] = None
    EMail: Optional[str] = None
    edificioDomFiscale: Optional[str] = None
    edificioDomicilio: Optional[str] = None
    edificioResidenza: Optional[str] = None
    esoneroObbligoResidenza: Optional[bool] = None
    fax: Optional[str] = None
    fornitoreCritico: Optional[bool] = None
    frazioneDomFiscale: Optional[str] = None
    frazioneDomicilio: Optional[str] = None
    frazioneResidenza: Optional[str] = None
    genere: Optional[str] = None
    idInterno: Optional[int] = None
    indirizzoDomFiscale: Optional[str] = None
    indirizzoDomicilio: Optional[str] = None
    indirizzoResidenza: Optional[str] = None
    indirizzoUtente: Optional[str] = None
    matricola: Optional[str] = None
    nome: Optional[str] = None
    note: Optional[str] = None
    noteRisorsaUmana: Optional[str] = None
    numeroDocIdentita: Optional[str] = None
    PEC: Optional[str] = None
    partitaIva: Optional[str] = None
    partitaIvaEstero: Optional[str] = None
    percCategoriaProtetta: Optional[int] = None
    postaElettronicaPrivata: Optional[str] = None
    postaElettronicaUfficio: Optional[str] = None
    psCodQuestura: Optional[str] = None
    psDataFine: Optional[datetime] = None
    psDataInizio: Optional[datetime] = None
    psDataPres: Optional[datetime] = None
    psMotivo: Optional[str] = None
    psNote: Optional[str] = None
    psNumero: Optional[str] = None
    psStato: Optional[str] = None
    quartiereDomFiscale: Optional[str] = None
    quartiereDomicilio: Optional[str] = None
    quartiereResidenza: Optional[str] = None
    le: Optional[bool] = None
    rifUfficio: Optional[str] = None
    secondoNome: Optional[str] = None
    skype: Optional[str] = None
    statoCivile: Optional[str] = None
    telCasa: Optional[str] = None
    telDomicilio: Optional[str] = None
    telUfficio: Optional[str] = None
    telefonoUtente1: Optional[str] = None
    telefonoUtente2: Optional[str] = None
    urlSitoWeb: Optional[str] = None
    urlcv: Optional[str] = None
    userAlias: Optional[str] = None
    username: Optional[str] = None
    utenteBloccato: Optional[int] = None
    utenteLDAP: Optional[int] = None
    utentePwdScaduta: Optional[int] = None
