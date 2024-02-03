## Le correcteur: comment ça fonctionne ?

Nous utilisons une instance hébergée par nos soins de [languagetool.org](https://languagetool.org), un correcteur français open source !

> ![NOTE]
> This project is not developed by Remède, please refer to the official website for any help and documentation...

## Lancer le conteneur

```shell
docker run -d \
  --name remede-corrector \
  --restart always \
  --cap-drop ALL \
  --cap-add CAP_SETUID \
  --cap-add CAP_SETGID \
  --security-opt no-new-privileges \
  --publish 9009:8010 \
  --env download_ngrams_for_langs=fr \
  --env langtool_languageModel=/ngrams \
  --env langtool_fasttextModel=/fasttext/lid.176.bin \
  --volume $PWD/ngrams:/ngrams \
  --volume $PWD/fasttext:/fasttext \
  meyay/languagetool:latest
```

## Documentation pour l'API
```
```

## Références

- Schéma de l'infrastructure [`INFRASTRUCTURE.md`](../INFRASTRUCTURE.md)
- Crédits des données Remède ; [documentation](../docs/FR.md#données-remède)
