FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf

RUN apt-get update

RUN apt-get install -y net-tools

RUN apt-get install -y keepalived

#COPY keepalived_backup.conf /etc/keepalived/keepalived.conf

COPY check_nginx.sh /etc/keepalived/check_nginx.sh

RUN chmod +x /etc/keepalived/check_nginx.sh

CMD ["service", "keepalived", "start"]

ENTRYPOINT nginx -g "daemon off;"