## TTS engine

> [!IMPORTANT]
> As discussed [here](https://github.com/camarm-dev/remede/discussions/65), it is better to use SSML but we didn't found any open source service which provides it.
> 
> So, we currently use [gmn/nanotts](https://github.com/gmn/nanotts), with [opentts](https://github.com/synesthesiam/opentts).


## How it works

We use docker the image `synesthesiam/opentts:fr` to deploy a server at [remede-tts.camarm.fr](https://remede-tts.camarm.fr).

It returns a WAVE file using the following POST request:
```http request
POST /api/tts?voice=nanotts%3Afr-FR&lang=fr&vocoder=high&denoiserStrength=0.0&text=<text-to-transform>&speakerId=&ssml=true&ssmlNumbers=false&ssmlDates=false&ssmlCurrency=false&cache=true
HTTP/1.1
Host: remede-tts.camarm.fr
```

Requests is executed in [app/src/components/WordModal.vue:386](../app/src/components/WordModal.vue).

- You should use these arguments to prevent container crashing 
```shell
docker run --name remede-tts --restart unless-stopped -d -p 5500:5500 synesthesiam/opentts:fr --no-glow-speak --no-larynx --no-espeak --no-marytts
```

## Goal

Utiliser le tag SSML `<phoneme alphabet="ipa" ph=""></phoneme>`.
