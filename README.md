# INFRANET


## Information bevor der Installation:

1. Python 3.6 required
2. Node required (einfach neuste Version ziehen)
3. ??? Windows Probleme

### Debian Pre Installations:

```console
chat@infranet:~$ sudo apt install pyvenv
chat@infranet:~$ sudo apt -y install libgconf2-4  #ist anscheinend auf Deb nicht standard, gibt sonst fehler.
```

### vor dem Clonen noch pruefen:

```console
chat@infranet:~$ node -v
chat@infranet:~$ npm -v
chat@infranet:~$ npm install -g yarn
```

### dann:

```console
chat@infranet:~$ git clone <hier ssh oder https von dem repo> #moeglicherweise muesst ihr euch noch ein ssh key anlegen
chat@infranet:~$ cd electron-react-python-app
chat@infranet:~$ pyvenv venv
chat@infranet:~$ source venv/bin/activate
chat@infranet:~$ yarn
chat@infranet:~$ yarn start

```

Die Anwendung sollte nun starten... wahrscheinlich 

das npm modul python-shell spielt hier eine wichtige rolle wie die beiden kommunizieren man koennte ja mal in die Doku schauen


## Link zum Tagebuch:
https://docs.google.com/spreadsheets/d/1TWkekIDpQT2U8OpKi3ymxciaGM6Ei_RP9KROXNjyts4/edit?usp=sharing