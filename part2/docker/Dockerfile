FROM joshjamison/python37:latest

ENV PATH="$V_ENV/bin:$PATH"

RUN git clone --single-branch --branch fastapi https://github.com/codemation/pyql-rest.git

RUN pip install -r pyql-rest/requirements.txt

WORKDIR /pyql-rest/pyql-rest/

EXPOSE 8190

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8190", "server:app"]