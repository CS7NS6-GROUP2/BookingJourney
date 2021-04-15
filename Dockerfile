FROM 1537f688c295

COPY . /app

WORKDIR /app

COPY nginx.conf /etc/nginx/nginx.conf

ENV VIRTUAL_ENV=venv

RUN python -m venv venv

#The most important part is setting PATH: PATH is a list of directories which are searched for commands to run. activate simply adds the virtualenv’s bin/ directory to the start of the list.
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

ENTRYPOINT nginx -g "daemon on;" && uwsgi --ini uwsgi.ini


