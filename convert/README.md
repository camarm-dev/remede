## Dictd server

Remède provides its own dictd server to serve simplificated versions of its database...

> [!WARNING]
> Execute all commands from project root.

### Setup ressources

To run properly, dictd needs dictionaries in a `.index` and `.dict` format.

These formats can be obtained from a `.txt` dictionary, with `dictfmt`
```shell
dictfmt -e -u https://github.com/camarm-dev/remede --utf8 --allchars -s "Remède" remede < remede.txt
```
The source `.txt` dictionary has a Special format :
```
<A NAME="word">
<B>word</B>
multiline
definition

<A NAME="word1">
<B>word1</B>
definition of word 2
```

The script `prepare.py` builds for each dictionary database (situated in `data/`) its `.txt` format in a compatible format,
then you can build `.index` and `.dict` ressources with `dictfmt`. Ressources are placed into `dictionaries/`.

Then, just run the docker commend below to start the Remède dictd instance.

> [!NOTE]
> You may need to install `dictfmt` using `apt install dictfmt`.
> You may also need to create the `convert/dictionaries` directory.

1. Prepare databases
```shell
python3 convert/prepare.py
```
2. Build ressources with `dictfmt` (move to the `convert/dictionaries` directory)
```shell
dictfmt -e --utf8 --allchars -s "Remède Français" remede < remede.txt
dictfmt -e --utf8 --allchars -s "Remède English" remede.en < remede.en.txt
```

### Start server

```shell
docker run -d --restart unless-stopped --name remede-convert -v ./convert/site.txt:/etc/dictd_site.txt -v ./convert/dictd.conf:/etc/dictd.conf -v ./convert/dictionaries:/usr/lib/dict -p 2628:2628 amaccis/dict
```

### More formats

We also release our dictionaries as XML Dictionary eXchange Format, or CSV. We juste generate the DICT dictionaries and convert
them using [pyglossary](https://github.com/ilius/pyglossary).

```shell
pyglossary convert/dictionaries/remede.index convert/dictionaries/remede.csv --read-format=DictOrg --write-format=Csv
pyglossary convert/dictionaries/remede.en.index convert/dictionaries/remede.en.csv --read-format=DictOrg --write-format=Csv
```

For **XDXF**, there is the `xdxf.py` script. Like the `prepare.py` script, it read and convert Remède dictionaries to XDXF.

List of the support keys :
- 
- 
