module.exports = {
  packagerConfig: {
    asar: true,
  },
  rebuildConfig: {},
  makers: [
    {
      name: '@electron-forge/maker-squirrel',
      config: {
        name: "Remède",
        manufacturer: "Labse Software",
        description: "Open source and free French dictionary !",
        iconUrl: "./assets/appIcon.ico",
        author: "Armand CAMPONOVO (@camarm-dev)"
      },
    },
    {
      name: '@electron-forge/maker-dmg',
      config: {
        name: "Remède",
        background: './assets/splash.png',
        format: 'ULFO',
        icon: "./assets/appIcon.ico"
      }
    },
    {
      name: '@electron-forge/maker-zip',
      platforms: ['darwin'],
    },
    {
      name: '@electron-forge/maker-deb',
      config: {
        options: {
          name: "remede",
          description: "Open source and free French dictionary !",
          productName: "Remède",
          productDescription: "Remède is an open source alternative to Antidote. It's free and open source !",
          categories: ["Utility"],
          genericName: "Dictionary",
          homepage: "https://remede.camarm.fr",
          icon: "./assets/appIcon.ico",
          maintainer: "Armand CAMPONOVO (@camarm-dev)"
        }
      },
    },
    {
      name: '@electron-forge/maker-rpm',
      config: {
        options: {
          name: "remede",
          description: "Open source and free French dictionary !",
          productName: "Remède",
          productDescription: "Remède is an open source alternative to Antidote. It's free and open source !",
          categories: ["Utility"],
          genericName: "Dictionary",
          homepage: "https://remede.camarm.fr",
          icon: "./assets/appIcon.ico",
          maintainer: "Armand CAMPONOVO (@camarm-dev)",
          license: "CeCill V2.1"
        }
      },
    },
  ],
  plugins: [
    {
      name: '@electron-forge/plugin-auto-unpack-natives',
      config: {},
    },
  ],
};
