FROM python:3.9

COPY . /app

WORKDIR /app

RUN python3 -m venv venv

#The most important part is setting PATH: PATH is a list of directories which are searched for commands to run. activate simply adds the virtualenv’s bin/ directory to the start of the list.
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

CMD ["uwsgi", "uwsgi.ini"]

#ENTRYPOINT nginx -g "daemon on;" &&

