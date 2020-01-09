# INFRANET

## [The procuct can be downloaded from the releases Page](https://github.com/stubifox/INFRANET/releases)


```diff
- DISCLAIMER!!!:
  The Product is only tested with dedicated Hardware from Speed Studio. Also the Code written is customized for this specific Hardware.
  This Product is not Sponsored by the Hardware Company.
  If you want to purchase the tested Hardware, you will need an Infrared Emitter and an Infrared Sender from Seed Studio.
  If you want to use you Own Infrared Sensors you might experience Bugs or a no functionality at all.
  Opening a new Issue is very welcome.
```


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
chat@infranet:~$ git clone <ssh or https of this repo>
chat@infranet:~$ cd INFRANET
chat@infranet:~$ python -m venv venv
chat@infranet:~$ source venv/bin/activate #Linux or Mac
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
