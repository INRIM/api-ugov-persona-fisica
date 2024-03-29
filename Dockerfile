FROM tiangolo/uvicorn-gunicorn:python3.11



LABEL maintainer="Alessio Gerace <a.gerace@inrim.it>"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir requests
RUN pip install --no-cache-dir aiohttp
RUN pip install --no-cache-dir lxml
RUN pip install --no-cache-dir xmltodict
RUN pip install --no-cache-dir ujson
RUN pip install --no-cache-dir python-jose[cryptography]
RUN pip install --no-cache-dir passlib[bcrypt]
RUN pip install --no-cache-dir zeep


