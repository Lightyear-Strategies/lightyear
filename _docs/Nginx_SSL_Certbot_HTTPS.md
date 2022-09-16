### Sources: 
_(configuration settings for ufw and nginx are found in the videos)_
* https://youtu.be/goToXTC96Co -- server settings (installing nginx)
* https://youtu.be/Gdys9qPjuKs -- SSL using certbot 
* https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal (installation guide for nginx)

* https://stackoverflow.com/questions/31682179/how-to-serve-flask-static-files-using-nginx
### Commands

To Control Uncomplicated Firewall:
* `sudo ufw default allow outgoing`
* `sudo ufw default deny incoming`
* `sudo ufw allow ssh`
* `sudo ufw allow http/tcp`
* `sudo ufw allow https/tcp`
* `sudo ufw allow 5000`
* `sudo ufw status`
* `sudo ufw enable`

Nginx:
* `sudo apt install nginx`
* `sudo rm /etc/nginx/sites-enabled/default`
* `sudo nano /etc/nginx/sites-enabled/lightyear`
* `sudo systemctl restart nginx`
* `sudo nano /etc/nginx/nginx.conf`
* `systemctl status nginx.service`

Certbot:
* `sudo certbot --nginx`

Gunicorn:
* `gunicorn -w 3 wsgi:app`


For Static Files:

```
location ^~ /static/  {
    include  /etc/nginx/mime.types;
    root /project_path/;
}
```

replace /project_path/ with your app's absolute path, you should note that it doesn't include static directory and all the contents inside /project_path/static/ will be serverd in url /static/.
