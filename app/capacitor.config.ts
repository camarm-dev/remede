import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'dev.camarm.remede',
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
  }
};

export default config;
