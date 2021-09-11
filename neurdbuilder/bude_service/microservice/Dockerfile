FROM gcr.io/google.com/cloudsdktool/cloud-sdk:latest


ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install google-python-cloud-debugger


ENTRYPOINT ["python3", "main.py"]
