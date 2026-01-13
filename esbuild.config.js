#!/usr/bin/env node

/**
 * Esbuild configuration for FreedomPay Integration
 * This app has no frontend assets, so we provide an empty configuration
 * that tells esbuild there's nothing to build.
 */

module.exports = {
  // Empty configuration - no files to build
  entryPoints: [],
  bundle: false,
  outfile: '',
  platform: 'browser',
  format: 'iife',

  // Plugin to handle the case where no assets exist
  plugins: [
    {
      name: 'freedompay-no-assets',
      setup(build) {
        build.onStart(() => {
          const messages = {
            en: 'FreedomPay Integration: No frontend assets to build - skipping esbuild',
            ru: 'FreedomPay Integration: Нет фронтенд-активов для сборки - пропуск esbuild',
            es: 'FreedomPay Integration: Sin activos frontend para compilar - omitiendo esbuild'
          };

          // Detect language and log appropriate message
          const lang = process.env.LANG || 'en';
          if (lang.startsWith('ru')) {
            console.log(messages.ru);
          } else if (lang.startsWith('es')) {
            console.log(messages.es);
          } else if (lang.startsWith('uz')) {
            console.log('FreedomPay Integration: Yigʻish uchun frontend aktivlari mavjud emas - esbuildni oʻtkazib yuborish');
          } else {
            console.log(messages.en);
          }
        });

        build.onEnd(() => {
          console.log('Build completed successfully (no assets)');
        });
      }
    }
  ]
};
