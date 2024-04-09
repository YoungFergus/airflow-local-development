ARG AIRFLOW_VERSION
FROM apache/airflow:${AIRFLOW_VERSION}
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt