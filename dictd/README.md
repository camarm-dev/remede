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
The source `.txt` dictionary has a [Jargon File](https://en.wikipedia.org/wiki/Jargon_File) format :
```
:word1:definition 1
:word2:definition 2
```

The script `prepare.py` builds for each dictionary database (situated in `data/`) its `.txt` format in a compatible format,
then you can build `.index` and `.dict` ressources with `dictfmt`. Ressources are placed into `dictionaries/`.

Then, just run the docker commend below to start the Remède dictd instance.

> [!NOTE]
> You may need to install `dictfmt` using `apt install dictfmt`.
> You may also need to create the `dictd/dictionaries` directory.

1. Prepare databases
```shell
python3 dictd/prepare.py
```
2. Build ressources with `dictfmt` (move to the `dictd/dictionaries` directory)
```shell
dictfmt -e --utf8 --allchars -s "Remède Français" remede < remede.txt
dictfmt -e --utf8 --allchars -s "Remède English" remede.en < remede.en.txt
```

### Start server

```shell
docker run -d --restart unless-stopped --name remede-dictd -v ./dictd/site.txt:/etc/dictd_site.txt -v ./dictd/dictd.conf:/etc/dictd.conf -v ./dictd/dictionaries:/usr/lib/dict -p 2628:2628 amaccis/dict
```

### More formats

We also release our dictionaries as XML Dictionary eXchange Format. We juste generate the DICT dictionaries and convert
them using [pyglossary](https://github.com/ilius/pyglossary).
