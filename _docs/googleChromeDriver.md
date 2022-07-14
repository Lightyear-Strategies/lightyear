Sources:
1. https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
2. https://stackoverflow.com/questions/48649230/how-to-update-chromedriver-on-ubuntu
3. https://www.linuxjournal.com/content/how-can-you-install-google-browser-debian


### Install ChromeDriver
```
version=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
wget -qP /tmp/ "https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip"
sudo unzip -o /tmp/chromedriver_linux64.zip -d /home/ubuntu/.local/bin
sudo chmod 755 /home/ubuntu/.local/bin/chromedriver
```
LATEST_RELEASE can be a specific version for example 103.0.5060.53-1

To check its version: `chromedriver --version`


### Install Google Chrome

One way:
```
sudo apt-get install google-chrome-stable
```
If you want to install a specific version of Chrome:
```
 wget "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_{VERSION}_amd64.deb"
 sudo apt install ./google-chrome-stable_{VERSION}_amd64.deb
```

E.g.:
```
wget "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_103.0.5060.53-1_amd64.deb"
sudo apt install google-chrome-stable_103.0.5060.53-1_amd64.deb
```

To check its version: `google-chrome-stable --version`