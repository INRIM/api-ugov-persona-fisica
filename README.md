# API Integrazione U-GOV JP - WSACPersonaFisica (SOAP)

API REST per l'integrazione con WSACPersonaFisica (SOAP) di U-GOV JP

Questo progetto è un componentne del progetto più ampio di un gruppo
di microservizi mirati all'integrazione con U-GOV, e possibile attivarli
singolarmente in modo modulare, e attivarne molteplici in modo scalare in caso di necessità


## Come iniziare

Clonare il progetto

- #### Configurazione 
    - creare una copia di .env.example:
      ```
        cp .env.json.example  app/.env
        ```
  
- #### Url Ambienti U-GOV

  Editare la chiave `BASE_URL_WS` file .env inserendo la url di pre-prod o prod di U-GOV
  come descritto nelle linee guida della documentazione del Technical Portal di U-GOV
  
- #### JWT Token e Autenticazione WS U-GOV
    
  Al fine di utilizzare i WS U-GOV è necessario attivare un utente tecnico abilitato allo scopo sullo stesso U'GOV.

  Abilitato l'utente U-GOV è necessario creare un token [JWT](https://jwt.io/) con tali informazioni da inviare alle API:
  
    - editare `JWT_SECRET` nel file .env aggiungendo la chiave segreta
      
      - e' possibile generare una chiave compatibile digitando: 
        ```
        openssl rand -hex 32
        ```
        
    - il token JWT, nel payload deve contenere:
      
      - ```
        {
            "sub": ugov_tech_user_name,
            "pass": ugov_tech_user_pass
        }
        ```
  - tuttavia e' possibile generare un token pronto all'uso eseguendo una chiamata in post al
    servizio: {url}/genera-token
    
    - ```
      payload:
      
      {
            "user": ugov_tech_user_name,
            "pass": ugov_tech_user_pass,
            "secret": secret_key,
            "alg": HS256
      }
      ```
    
- #### Ambiente di Sviluppo
    
    Assicurarsi di avere Doclker Installato
    
    Se necessario modificare il binding porta 8022
  
    ```
    sh build_and_run.sh
    ```
  
    il servizio si avvia avvia http://localhost:8022/
  
    lo script abilita autoreload dei file per semplificare la fase di sviluppo


- #### Ambiente di Test / Pre-Produzione

  Assicurarsi di avere Docker Installato ed eseguire `sh build_and_run_test.sh`

  E' possibile modificare:
  
    - binding porta 8022 `-p 8022:80`
    - il numero di Worker editando  `WEB_CONCURRENCY=1`
  
  Il reverse Proxy e' deleagato ad un webserver ad esempio Nginx
  
  il servizio si avvia avvia http://{url}:8022/

- #### Ambiente di Produzione

  Assicurarsi di avere Docker Installato ed eseguire `sh build_and_run_prod.sh`

  E' possibile modificare:
  
    - binding porta 8022 `-p 8022:80`
    - il numero di Worker editando  `WEB_CONCURRENCY=1`
  
  Per il calcolo del numero di worker eseguire la seguente operazione `(CPU x 2)+1`
  
  Il reverse Proxy e' deleagato ad un webserver ad esempio Nginx
  
  il servizio si avvia avvia http://{url}:8022/


## Documentazione e Test delle Api

Una volta avviato il progetto la documentazione delle API è disponibile agli url:

- {BASE_URL}:8022/redoc ( Redoc )
- {BASE_URL}:8022/docs ( Swagger )

Tramite la Documentazione Swagger e' possibile testare le API:

- {BASE_URL}:8022/docs

Per eseguire i test e' necessario inserire come parametro header il token JWT generato

## Costruito con

* [FastApi](https://https://fastapi.tiangolo.com/.tiangolo.com/) - The Api framework 
* [Docker](https://docs.docker.com/) 

## Versionamento

Usiamo [SemVer](http://semver.org/) per il versionamento. Versioni disponibili, vedere [tags in questo repository](https://github.com/INRIM/api-ugov-persona-fisica/tags). 


## Licenza

api-ugov-persona-fisica è rilasciato con [licenza MIT](https://github.com/INRIM/api-ugov-persona-fisica/blob/master/LICENSE).