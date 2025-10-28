FROM python:3.12-slim

RUN apt update
RUN apt install -y apache2
RUN mkdir /var/www/FlaskApp
RUN mkdir /var/www/FlaskApp/FlaskApp 

WORKDIR /var/www/FlaskApp

COPY ./flaskapp.wsgi ./
COPY ./app.py ./FlaskApp/
COPY ./templates ./FlaskApp/templates
COPY ./public_key.pem ./FlaskApp/
COPY ./requirements.txt ./FlaskApp/
COPY ./.env ./FlaskApp/
COPY ./flask.conf /etc/apache2/sites-available/

RUN apt install -y libapache2-mod-wsgi-py3 python3.13-venv
RUN a2enmod ssl
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt -subj "/C=LS/ST=Noord-Brabant/L=Eindhoven/O=Random Org./CN=localhost"
RUN python3.13 -m venv venv
RUN ./venv/bin/python -m pip install -r ./FlaskApp/requirements.txt
RUN apachectl -k restart
RUN chown -R www-data:www-data /var/log/apache2/
RUN chown -R www-data:www-data /var/www/FlaskApp/
RUN find /var/www/FlaskApp/ -type d -exec chmod 755 {} \;
RUN find /var/www/FlaskApp/ -type f -exec chmod 644 {} \;
RUN a2ensite flask



EXPOSE 80
EXPOSE 443

HEALTHCHECK --interval=5m --timeout=3s CMD [ "curl","-f"," http://localhost/", "||", "exit", "1"]

CMD ["apachectl", "-D", "FOREGROUND"]


