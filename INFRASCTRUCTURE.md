# Infrastructure

This file is updated when the infrastructure changes. It shows a schema of the current infrastructure.

```mermaid
graph LR
    subgraph "`fa:fa-user User side`"
        J[(Database)] <-.-> A((User))
    end
    subgraph "`fa:fa-server Server side`"
        subgraph fa:fa-circle-nodes Proxy
            A((User)) --> B([Load Balancer])
        end
        subgraph fa:fa-memory Dedicated VM
            B --> C[API]
            B --> D[Ionic Web]
        end
        subgraph docker["`fa:fa-docker Dedicated Docker Server`"]
            B --> G[TTS service]
            B -.-> H[Corrector service]
            B -.-> L[Rimes graph service]
        end
        subgraph fa:fa-folder Filesystem
            C --> E[(Database)]
            E --> F[JSON]
        end
    end

```

## Image on mermaid.live

[![](https://mermaid.ink/img/pako:eNqFk-FugjAUhV-l6S9IZA9gliUqc9PoZsRtyQqJtb1oI1BTYJEY330X2FAjc_0Bze3Xe04OlwMVWgLt0rXhuw2ZzP2E4ErzVV3w6TLk3ZA7eQqGvJWPVElY-rQGyzVmlsszvuIp2AG5d-6cB9KzrBK27RqDRP7VGKkv7OrVr6vmzYWaFsqICJwETadkZvS-OKHlanSJgy76FptoLkmfRzwRYAL7RDeWWlRiiLUpiAtSCZ6BJO_TS5l-1X7AerNR0HbispFOlCAfsAr-k5RabMGwJpCV3p8pu9XpTzyYTKvcE1ssPFImqQRcE-UHeWYDbQyITJvb4ITNVYzh1uau0Vu5hTqSaHaoIkiLNIP4UmFQmX08H5dL4LEChmzsvb60SeKGdmgMJuZK4tAeyrJPsw3E4NMubiU323J8jsjxPNNekQjazUwOHZrvJEbqKo6W498iBo2RTOufQOgkVGu8uuPJp9YIhTxK4fgNaNbrOw?type=png)](https://mermaid.live/edit#pako:eNqFk-FugjAUhV-l6S9IZA9gliUqc9PoZsRtyQqJtb1oI1BTYJEY330X2FAjc_0Bze3Xe04OlwMVWgLt0rXhuw2ZzP2E4ErzVV3w6TLk3ZA7eQqGvJWPVElY-rQGyzVmlsszvuIp2AG5d-6cB9KzrBK27RqDRP7VGKkv7OrVr6vmzYWaFsqICJwETadkZvS-OKHlanSJgy76FptoLkmfRzwRYAL7RDeWWlRiiLUpiAtSCZ6BJO_TS5l-1X7AerNR0HbispFOlCAfsAr-k5RabMGwJpCV3p8pu9XpTzyYTKvcE1ssPFImqQRcE-UHeWYDbQyITJvb4ITNVYzh1uau0Vu5hTqSaHaoIkiLNIP4UmFQmX08H5dL4LEChmzsvb60SeKGdmgMJuZK4tAeyrJPsw3E4NMubiU323J8jsjxPNNekQjazUwOHZrvJEbqKo6W498iBo2RTOufQOgkVGu8uuPJp9YIhTxK4fgNaNbrOw)