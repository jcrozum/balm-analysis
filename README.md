# balm-analysis
Analyses of Boolean networks that showcase the Boolean Attractor Landscape Mapper (balm)

# requirements
Requires `balm` and all its dependencies. See https://github.com/jcrozum/balm.
Only Linux is supported. Users on Windows should use WSL2.

## instructions for setup
1. It is recommended that you initialize a virtual environment, e.g., using
```
$ python3 -m venv .venv && source .venv/bin/activate
```


2. Intsall `balm` Python dependencies:
```
$ pip3 install -r requirements.txt
```

3. Install `gringo`, e.g. using
```
$ sudo apt install gringo
```

4. Install `pint` from https://github.com/pauleve/pint. On Ubuntu, for example, you can run this:
```
$ wget https://github.com/pauleve/pint/releases/download//2019-05-24/pint_2019-05-24_amd64.deb
$ sudo apt install ./pint_2019-05-24_amd64.deb
```

5. Install `mole` from http://www.lsv.fr/~schwoon/tools/mole/, e.g. using this:
```
$ wget http://www.lsv.fr/~schwoon/tools/mole/mole-140428.tar.gz
$ tar -xvf mole-140428.tar.gz
$ (cd ./mole-140428 && make)
```
Note that you will need to make sure that the `mole` command is added to your `PATH`.

6. Install `balm`, e.g.
```
$ pip3 install git+https://github.com/jcrozum/balm
```