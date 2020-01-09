# INFRANET

### The final Product can be downloaded from the Releases Page.

## Development:
## Informations before installing:

1. Python 3.6 required
2. Node required (newest Version)

### Debian Pre Installations:

```console
chat@infranet:~$ sudo apt install pyvenv
chat@infranet:~$ sudo apt -y install libgconf2-4  #ist anscheinend auf Deb nicht standard, gibt sonst fehler.
```

### Check before Cloning:

```console
chat@infranet:~$ node -v
chat@infranet:~$ npm -v
chat@infranet:~$ npm install -g yarn
```

### Setting up the environment:

```console
chat@infranet:~$ git clone <hier ssh oder https von dem repo> #moeglicherweise muesst ihr euch noch ein ssh key anlegen
chat@infranet:~$ cd INFRANET
chat@infranet:~$ python -m venv venv
(chat@infranet:~$ source venv/bin/activate #Linux oder Mac)
chat@infranet:~$ source venv/Scripts/activate #Windows
chat@infranet:~$ yarn
chat@infranet:~$ yarn start

```

The Application should start now. It might happen, that you need to install required Python moudules manually using pip3.

## Deployment:

```
$ yarn package-windows
$ yarn package-debian
```



## Link for Hour-Management:
https://docs.google.com/spreadsheets/d/1TWkekIDpQT2U8OpKi3ymxciaGM6Ei_RP9KROXNjyts4/edit?usp=sharing
