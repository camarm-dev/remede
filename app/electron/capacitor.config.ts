import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.camarm.remede',
  appName: 'Remède',
  webDir: 'dist',
  plugins: {
    "SplashScreen": {
      "launchAutoHide": false,
      "androidScaleType": "CENTER_CROP",
      "splashFullScreen": true,
      "splashImmersive": false,
      "backgroundColor": "#ffffff"
    },
    CapacitorHttp: {
      enabled: false
    }
  },
  server: {
    androidScheme: 'https'
  },
  electron: {
    deepLinkingEnabled: true,
    deepLinkingCustomProtocol: 'remede',
    splashScreenImageName: "splash.png",
    splashScreenEnabled: true,
    customUrlScheme: 'remede'
  }
};

export default config;
