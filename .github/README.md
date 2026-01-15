# DO NOT USE THIS NO MORE

It's dumb, not maintained and there is an official API now that is much more stable. See: https://vyuka.gyarab.cz/api/

![repository logo](./assets/repologo.svg)


<div id="badges">
    <a href="https://gyarab.cz">
        <img alts="GyArab website" src="https://img.shields.io/badge/Gymnázium Arabská-blue?style=for-the-badge">
    </a>
    <img alts="Last Github Commit" src="https://img.shields.io/github/last-commit/CodyMarkix/GAVServer?style=for-the-badge">
    <img alt="Github Stars" src="https://img.shields.io/github/stars/CodyMarkix/GAVServer?style=for-the-badge">
    <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/markix124/gavserver?style=for-the-badge">
</div>

<br>

GAV Server je neoficiální API napsaná v Pythonu určena pro jednoduchou interakci se serverem [Gyarab výuka](https://vyuka.gyarab.cz). 

# Instalace

## Prerequisites
- pyenv (**doporučován** ale nepovinný)
- Flask
- selenium
- selenium-requests
- flassger
- flassger-RESTful

### Do production

- nginx (prosím mi někdo řekněte kdo reálně používá Apache v production)
- váš oblíbený WSGI server! Unit soubory v [/services/](../services/) očekávají [gunicorn](https://pypi.org/project/gunicorn).

## Instalační proces

1) Naklonujte repozitář a vstupte do něj

```bash
git clone https://github.com/CodyMarkix/GAVServer.git && GAVServer
```

2) Vytvořte venv v kořenu projektu

```bash
python3 -m venv .venv
```

3) Nainstalujte závislosti

```
pip install -r requirements/prod.txt
```

Pokud neplánujete hostovat svoji vlastní instaci, stačí závislosti z `common.txt`.

4) Přepiště si unit soubory jak je libo (pokud nevíte co děláte, prostě to nedělejte) a zkopírujte je do systemd složky.
```
sudo cp ./services/gunicorn.* /etc/systemd/system/
```

5) Zkopírujte nginx konfiguraci do nginx složky
```bash
sudo cp ./services/gavserver_nginx /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/gavserver_nginx /etc/nginx/sites-enabled/gavserver_nginx
```

6) Spusťte server!

```bash
systemctl enable gunicorn.socket --now
systemctl enable gunicorn.service --now

sudo nginx -t
systemctl start nginx
```

# Stavění ze zdrojáku

![](https://media1.tenor.com/m/PG7TQGmTPoMAAAAd/are-you-serious-spiderman.gif)

# Contributing

TODO: Write a contributing section, it's 1 AM and I have a chem test tomorrow I'm not gonna bother right now
