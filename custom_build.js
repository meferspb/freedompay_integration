#!/usr/bin/env node

/**
 * Multilingual Custom Build Script for FreedomPay Integration
 * Supports multiple languages and proper error handling
 */

const i18n = {
  en: {
    noBuildRequired: 'FreedomPay Integration: No build required (no frontend assets)',
    buildSkipped: 'Build process skipped successfully',
    errorOccurred: 'Build error occurred'
  },
  ru: {
    noBuildRequired: 'FreedomPay Integration: Сборка не требуется (нет фронтенд-активов)',
    buildSkipped: 'Процесс сборки успешно пропущен',
    errorOccurred: 'Произошла ошибка сборки'
  },
  es: {
    noBuildRequired: 'FreedomPay Integration: No se requiere compilación (sin activos frontend)',
    buildSkipped: 'Proceso de compilación omitido correctamente',
    errorOccurred: 'Ocurrió un error de compilación'
  },
  uz: {
    noBuildRequired: 'FreedomPay Integration: Yigʻish talab qilinmaydi (frontend aktivlari yoʻq)',
    buildSkipped: 'Yigʻish jarayoni muvaffaqiyatli oʻtkazib yuborildi',
    errorOccurred: 'Yigʻishda xatolik yuz berdi'
  }
};

function getLanguage() {
  // Detect language from environment or use default
  const lang = process.env.LC_ALL || process.env.LC_MESSAGES || process.env.LANG || 'en';
  if (lang.startsWith('ru')) return 'ru';
  if (lang.startsWith('es')) return 'es';
  if (lang.startsWith('uz')) return 'uz';
  return 'en';
}

function main() {
  try {
    const lang = getLanguage();
    console.log(i18n[lang].noBuildRequired);
    console.log(i18n[lang].buildSkipped);
    process.exit(0);
  } catch (error) {
    console.error(i18n.en.errorOccurred, error.message);
    process.exit(1);
  }
}

main();
