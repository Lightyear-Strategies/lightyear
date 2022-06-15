Connect to server via SSH:
https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-ssh-using-terminal

1. Give permissions to the private key. Download it from the Amazon
    sudo chmod 400 /Users/rutkovskii/Desktop/lys/LightsailDefaultKey-ca-central-1.pem
2. SSH using private key into <user>@<server's ip>
    ssh -i /Users/rutkovskii/Desktop/lys/LightsailDefaultKey-ca-central-1.pem ubuntu@99.79.179.105

Installing Python 3.8.10:
https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/

1. Update the packages list and install the packages necessary to build Python:
    sudo apt update
    sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

2. Download the latest release’s source code from the Python download page using wget :
    wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz

3. When the download finishes, extract the gzipped archive :
    tar -xf Python-3.8.10.tgz
4. Switch to the Python source directory and execute the configure script which performs a number of checks to make sure
   all of the dependencies on your system are present:
    cd Python-3.8.10
    ./configure --enable-optimizations

5. Start the Python 3.8 build process:
(number after -j corresponds to number of cores, to find number of cores run "nproc")
    make -j 1

6. When the build process is complete, install the Python binaries by typing:
    sudo make altinstall

7. That’s it. Python 3.8 has been installed and ready to be used. Verify it by typing:
    python3.8 --version



Solving issue of

 ```
 The conflict is caused by:
    celery[sqs] 5.2.3 depends on kombu<6.0 and >=5.2.3
    celery 5.2.3 depends on kombu<6.0 and >=5.2.3
    kombu[sqs] 4.6.11 depends on kombu 4.6.11 (Installed)
    kombu[sqs] 5.2.3 depends on pycurl~=7.44.1; extra == "sqs"
 ```

 by installing: sudo apt install libcurl4-openssl-dev libssl-dev