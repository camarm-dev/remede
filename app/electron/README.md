## Electron

Ressources generated by `npx cap add @capacitor-community/electron`

### Updated changes

```shell
npx cap sync @capacitor-community/electron
```

### Run electron app

```shell
npx cap open @capacitor-community/electron
```

### Build

[Electron documentation](https://www.electronjs.org/docs/latest/tutorial/tutorial-packaging)

```shell
npm run make
```

### Multiplatform build

**Build EXE, DEB and RPM; on a Linux system**

- Dependencies
```shell
apt install mono-devel wine
```

- _Linux platforms_
```shell
npm run make
```

- _Windows exe_
```shell
npm run make -- --platform win32
```

**Build DMG; using docker**

// In development //

```shell
docker run sickcodes/docker-osx:naked
```