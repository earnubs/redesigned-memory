from python:3.7

RUN pip install --upgrade pipenv==2018.11.26

WORKDIR /usr/src/app

# create non-root user to run our app.
RUN useradd -ms /bin/bash app

USER app
