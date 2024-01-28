## Le correcteur: comment ça fonctionne ?

Ce dossier contient le code source de [grammalecte](https://grammalecte.net/), un correcteur français open source !

> ![NOTE]
> This project is not developed by Remède, please refer to the official website for any help and documentation...

## Lancer le conteneur

```shell
docker build -t grammalecte:latest .
```

```shell
docker run --rm -p 9009:8080 --name remede-corrector grammalecte:latest
```

## Références

- Schéma de l'infrastructure [`INFRASTRUCTURE.md`](../INFRASCTRUCTURE.md)
- Crédits des données Remède ; [documentation](../docs/FR.md#données-remède)
