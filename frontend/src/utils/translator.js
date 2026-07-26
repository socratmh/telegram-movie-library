/**
 * Utility to translate user-defined library names and media titles between Arabic and English.
 */

// Bidirectional exact/common title dictionary
const DIRECTORY_MAP = {
  // Arabic -> English
  'مسلسلات أجنبية': 'Foreign TV Series',
  'مسلسلات اجنبية': 'Foreign TV Series',
  'أفلام أجنبية': 'Foreign Movies',
  'افلام اجنبية': 'Foreign Movies',
  'مسلسلات عربية': 'Arabic TV Series',
  'أفلام عربية': 'Arabic Movies',
  'افلام عربية': 'Arabic Movies',
  'مسلسلات تركية': 'Turkish TV Series',
  'أفلام تركية': 'Turkish Movies',
  'افلام تركية': 'Turkish Movies',
  'مسلسلات كورية': 'Korean TV Series',
  'أفلام كورية': 'Korean Movies',
  'افلام كورية': 'Korean Movies',
  'مسلسلات هندية': 'Indian TV Series',
  'مسلسلات هندي': 'Indian TV Series',
  'أفلام هندية': 'Indian Movies',
  'افلام هندية': 'Indian Movies',
  'أفلام هندي': 'Indian Movies',
  'مسلسلات آسيوية': 'Asian TV Series',
  'مسلسلات اسيوية': 'Asian TV Series',
  'أفلام آسيوية': 'Asian Movies',
  'افلام اسيوية': 'Asian Movies',
  'مسلسلات أنمي': 'Anime TV Series',
  'مسلسلات انمي': 'Anime TV Series',
  'أفلام أنمي': 'Anime Movies',
  'افلام انمي': 'Anime Movies',
  'أنمي': 'Anime',
  'انمي': 'Anime',
  'وثائقيات': 'Documentaries',
  'مسلسلات وثائقية': 'Documentary TV Series',
  'أفلام وثائقية': 'Documentary Movies',
  'افلام وثائقية': 'Documentary Movies',
  'مسلسلات مدبلجة': 'Dubbed TV Series',
  'أفلام مدبلجة': 'Dubbed Movies',
  'افلام مدبلجة': 'Dubbed Movies',
  'مسلسلات رمضان': 'Ramadan TV Series',
  'أفلام كرتون': 'Animated Movies',
  'افلام كرتون': 'Animated Movies',
  'رسوم متحركة': 'Animation',
  'مسلسلات مكسيكية': 'Mexican TV Series',
  'أفلام مكسيكية': 'Mexican Movies',
  'افلام مكسيكية': 'Mexican Movies',

  // English -> Arabic
  'Foreign TV Series': 'مسلسلات أجنبية',
  'Foreign Series': 'مسلسلات أجنبية',
  'Foreign TV Shows': 'مسلسلات أجنبية',
  'Foreign Movies': 'أفلام أجنبية',
  'Foreign Movie': 'أفلام أجنبية',
  'Arabic TV Series': 'مسلسلات عربية',
  'Arabic Series': 'مسلسلات عربية',
  'Arabic Movies': 'أفلام عربية',
  'Turkish TV Series': 'مسلسلات تركية',
  'Turkish Series': 'مسلسلات تركية',
  'Turkish Movies': 'أفلام تركية',
  'Korean TV Series': 'مسلسلات كورية',
  'Korean Series': 'مسلسلات كورية',
  'Korean Movies': 'أفلام كورية',
  'Indian TV Series': 'مسلسلات هندية',
  'Indian Series': 'مسلسلات هندية',
  'Bollywood Series': 'مسلسلات هندية',
  'Indian Movies': 'أفلام هندية',
  'Bollywood Movies': 'أفلام هندية',
  'Asian TV Series': 'مسلسلات آسيوية',
  'Asian Series': 'مسلسلات آسيوية',
  'Asian Movies': 'أفلام آسيوية',
  'Anime TV Series': 'مسلسلات أنمي',
  'Anime Series': 'مسلسلات أنمي',
  'Anime Movies': 'أفلام أنمي',
  'Anime': 'أنمي',
  'Documentaries': 'وثائقيات',
  'Documentary TV Series': 'مسلسلات وثائقية',
  'Documentary Series': 'مسلسلات وثائقية',
  'Documentary Movies': 'أفلام وثائقية',
  'Dubbed TV Series': 'مسلسلات مدبلجة',
  'Dubbed Series': 'مسلسلات مدبلجة',
  'Dubbed Movies': 'أفلام مدبلجة',
  'Ramadan TV Series': 'مسلسلات رمضان',
  'Ramadan Series': 'مسلسلات رمضان',
  'Animated Movies': 'أفلام كرتون',
  'Animation Movies': 'أفلام كرتون',
  'Cartoons': 'رسوم متحركة',
  'Mexican TV Series': 'مسلسلات مكسيكية',
  'Mexican Series': 'مسلسلات مكسيكية',
  'Mexican Movies': 'أفلام مكسيكية',
};

// Word-level dictionaries for dynamic token translation
const AR_TO_EN_WORDS = {
  'مسلسلات': 'TV Series',
  'مسلسل': 'Series',
  'أفلام': 'Movies',
  'افلام': 'Movies',
  'فيلم': 'Movie',
  'فلم': 'Movie',
  'أجنبية': 'Foreign',
  'اجنبية': 'Foreign',
  'أجنبي': 'Foreign',
  'اجنبي': 'Foreign',
  'عربية': 'Arabic',
  'عربي': 'Arabic',
  'تركية': 'Turkish',
  'تركي': 'Turkish',
  'كورية': 'Korean',
  'كوري': 'Korean',
  'هندية': 'Indian',
  'هندي': 'Indian',
  'آسيوية': 'Asian',
  'اسيوية': 'Asian',
  'آسيوي': 'Asian',
  'اسيوي': 'Asian',
  'مكسيكية': 'Mexican',
  'مكسيكي': 'Mexican',
  'إسبانية': 'Spanish',
  'اسبانية': 'Spanish',
  'أنمي': 'Anime',
  'انمي': 'Anime',
  'وثائقية': 'Documentary',
  'وثائقي': 'Documentary',
  'وثائقيات': 'Documentaries',
  'مدبلجة': 'Dubbed',
  'مدبلج': 'Dubbed',
  'مترجمة': 'Subtitled',
  'مترجم': 'Subtitled',
  'رمضان': 'Ramadan',
  'كرتون': 'Cartoons',
  'أكشن': 'Action',
  'اكشن': 'Action',
  'دراما': 'Drama',
  'كوميديا': 'Comedy',
  'رعب': 'Horror',
  'غموض': 'Mystery',
  'خيال': 'Sci-Fi',
  'علمي': '',
  'رومانسية': 'Romance',
  'رومانسي': 'Romance',
  'عائلية': 'Family',
  'عائلي': 'Family',
  'مغامرات': 'Adventure',
  'مغامرة': 'Adventure',
  'مكتبة': 'Library',
};

const EN_TO_AR_WORDS = {
  'foreign': 'أجنبية',
  'arabic': 'عربية',
  'turkish': 'تركية',
  'korean': 'كورية',
  'indian': 'هندية',
  'bollywood': 'هندية',
  'asian': 'آسيوية',
  'mexican': 'مكسيكية',
  'spanish': 'إسبانية',
  'anime': 'أنمي',
  'documentary': 'وثائقية',
  'documentaries': 'وثائقيات',
  'dubbed': 'مدبلجة',
  'subtitled': 'مترجمة',
  'ramadan': 'رمضان',
  'cartoons': 'كرتون',
  'animation': 'رسوم متحركة',
  'animated': 'كرتونية',
  'action': 'أكشن',
  'drama': 'دراما',
  'comedy': 'كوميديا',
  'horror': 'رعب',
  'mystery': 'غموض',
  'sci-fi': 'خيال علمي',
  'romance': 'رومانسية',
  'family': 'عائلية',
  'adventure': 'مغامرات',
  'library': 'مكتبة',
  'movies': 'أفلام',
  'movie': 'فيلم',
  'series': 'مسلسلات',
  'tv': '',
  'shows': 'برامج',
};

const ARABIC_PATTERN = /[\u0600-\u06FF]/;

/**
 * Translates a library name based on the target language ('ar' or 'en').
 * If the input is already in the target language or unmapped, returns appropriate form.
 */
export function translateLibraryName(text, targetLang = 'en') {
  if (!text || typeof text !== 'string') return text || '';
  const trimmed = text.trim();
  if (!trimmed) return trimmed;

  // 1. Direct exact dictionary match
  if (DIRECTORY_MAP[trimmed]) {
    const mapped = DIRECTORY_MAP[trimmed];
    const mappedIsAr = ARABIC_PATTERN.test(mapped);
    if ((targetLang === 'ar' && mappedIsAr) || (targetLang === 'en' && !mappedIsAr)) {
      return mapped;
    }
  }

  // Check input language
  const inputIsAr = ARABIC_PATTERN.test(trimmed);

  // If already in target language, return as is
  if ((targetLang === 'ar' && inputIsAr) || (targetLang === 'en' && !inputIsAr)) {
    return trimmed;
  }

  // 2. Arabic -> English dynamic translation
  if (targetLang === 'en' && inputIsAr) {
    const tokens = trimmed.split(/\s+/);
    const translatedNouns = [];
    const translatedAdjectives = [];

    for (const token of tokens) {
      const match = AR_TO_EN_WORDS[token];
      if (match !== undefined) {
        if (match === '') continue;
        if (match === 'Movies' || match === 'TV Series' || match === 'Series' || match === 'Movie' || match === 'Documentaries' || match === 'Anime') {
          translatedNouns.push(match);
        } else {
          translatedAdjectives.push(match);
        }
      } else {
        translatedAdjectives.push(token);
      }
    }

    if (translatedNouns.length > 0 || translatedAdjectives.length > 0) {
      // English order: Adjective + Noun
      return [...translatedAdjectives, ...translatedNouns].join(' ');
    }
  }

  // 3. English -> Arabic dynamic translation
  if (targetLang === 'ar' && !inputIsAr) {
    // Check multi-word phrase patterns
    let workingText = trimmed;
    let nounPart = '';

    if (/tv\s+series/i.test(workingText)) {
      nounPart = 'مسلسلات';
      workingText = workingText.replace(/tv\s+series/i, '');
    } else if (/series/i.test(workingText)) {
      nounPart = 'مسلسلات';
      workingText = workingText.replace(/series/i, '');
    } else if (/movies/i.test(workingText)) {
      nounPart = 'أفلام';
      workingText = workingText.replace(/movies/i, '');
    } else if (/movie/i.test(workingText)) {
      nounPart = 'فيلم';
      workingText = workingText.replace(/movie/i, '');
    }

    const tokens = workingText.trim().split(/\s+/).filter(Boolean);
    const translatedAdjectives = [];

    for (const token of tokens) {
      const lower = token.toLowerCase();
      if (EN_TO_AR_WORDS[lower]) {
        if (EN_TO_AR_WORDS[lower] !== '') {
          translatedAdjectives.push(EN_TO_AR_WORDS[lower]);
        }
      } else {
        translatedAdjectives.push(token);
      }
    }

    if (nounPart || translatedAdjectives.length > 0) {
      // Arabic order: Noun + Adjectives
      return [nounPart, ...translatedAdjectives].filter(Boolean).join(' ');
    }
  }

  return trimmed;
}
