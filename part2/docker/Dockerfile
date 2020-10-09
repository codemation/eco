FROM joshjamison/python37:latest

ENV PATH="$V_ENV/bin:$PATH"

RUN git clone https://github.com/codemation/eco.git

WORKDIR /eco/part2/

RUN pip install -r /eco/part2/requirements.txt

WORKDIR /eco/part2/office_space

EXPOSE 8190

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8190", "server:app"]