FROM python:3.9
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . /

ENTRYPOINT ["streamlit", "run"]

CMD ["./pi_dz3.py"]

