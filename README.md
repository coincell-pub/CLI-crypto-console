Multiplexer
=============================

## About

Multiplexer is a CLI-based platform to buy, sell and get informations about cryptocurrencies.

The shell-like interface makes it easy to place orders, jump between different markets, see historic prices, and much more. It uses [GNU readline](https://tiswww.case.edu/php/chet/readline/rltop.html) under the hood to provide parameter autocompletion and command history so performing any actions is quick and easy.

Supported markets are currently Bittrex, Binance, and Kucoin.

### Dependencies

Installing the required dependencies is easy. Just clone this repo and run:

```bash
pip install -r requirements.txt
```

This command will install all the python dependencies you need via `pip` and you're ready to go.

### Configuration file

The configuration file has to be in [yaml](http://yaml.org/) format. In case you clone the repo, keep in mind the `configs` directory is inside `.gitignore` so it's safe to place files in there as they will never be committed into your repo.

A basic configuration file to use Bittrex would look like:

```yaml

exchanges:
  - name: bittrex
    api_key: 91220aacb69bc6401b1e04e290e022cd
    api_secret: 9c9e97f59eed930120633191a29bee5f
database:
  path: 'configs/config.db'
```

If you don't want to put your API keys in yet, you can simply set both fields to _null_. This will allow you to perform publicly accessible read operations like seeing order books, prices, etc.

The database path will be used to create a _sqlite3_ file to store some data. Currently only the address book is stored in it.

Note that you can set multiple exchange's keys, using different exchange names for them (e.g. "bittrex" and "binance"). If you specify multiple of them in your configuration file, you'll need to provide the one you want to use by using the `-e` parameter when running the shell.

#### Fiat currency support

Multiplexer will periodically poll [Coin Market Cap](https://coinmarketcap.com/) to pull coin prices. By default all prices will be shown in _USD_ but if you want to use some other fiat currency [supported by _CMC_](https://coinmarketcap.com/api/), then you can add an entry in your config file that looks like:

```yaml
metadata:
  fiat_currency: eur
```

#### Encrypting the configuration file

Given that the configuration file will contain your API keys, you may not want it to be stored in plain text on your filesystem. If that's the case, then you can use the `encryptor.py` script in the root of this project. It will encrypt your configuration file using AES in CFB mode and a passphrase you provide. Every time you run the shell, you'll have to provide the decryption key.

For example:

```bash
# This will encrypt the configs/config.yaml file and will emit the
# encrypted file into configs/config.yaml.encrypted
./encryptor.py -e -p configs/config.yaml  > configs/config.yaml.encrypted

# Now run the shell using -d (decrypt)
./multiplexer.py -c configs/config.yaml.encrypted -d
```

### Running the application

In order to run the application, just execute:

```bash
./multiplexer.py -c configs/config.yaml
```
