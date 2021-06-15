FROM python:3.7
ADD . /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python3 -m spacy download en_core_web_sm
CMD ["python", "login.py"]
