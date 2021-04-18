#!/bin/bash
# shellcheck disable=SC2006
#A=$(ps -C nginx --no-header | wc -l)
#if [ $A -eq 0 ]; then
#  /usr/local/nginx/sbin/nginx
#  # shellcheck disable=SC2046
#  if [ $(ps -C nginx --no-header | wc -l) -eq 0 ]; then
#    killall keepalived
#  fi
#fi
/usr/sbin/keepalived -n -l -D -f /etc/keepalived/keepalived.conf --dont-fork --log-console &
nginx -g "daemon off;"
