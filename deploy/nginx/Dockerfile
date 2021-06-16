FROM nginx:1.19-alpine

RUN rm -rf /etc/nginx/conf.d
COPY deploy/nginx/host.conf /etc/nginx/conf.d/default.conf