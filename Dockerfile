FROM python:3.7.9
WORKDIR /app

COPY requirement.txt .
RUN pip install -r requirement.txt
RUN rm requirement.txt

CMD [ "/bin/bash" ]
