import { useState, useEffect } from 'react';
import { fetchLibraries, fetchTVLibraries } from '../api/client';
import { translateLibraryName } from '../utils/translator';
import FeaturedSeriesSection from './FeaturedSeriesSection';

export default function LibraryGrid({ onSelectLibrary, onSelectTVLibrary, lang = 'en' }) {
  const [libraries, setLibraries] = useState([]);
  const [tvLibraries, setTvLibraries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const isAr = lang === 'ar';

  useEffect(() => {
    Promise.all([fetchLibraries(), fetchTVLibraries()])
      .then(([movieRes, tvRes]) => {
        setLibraries(movieRes.libraries || []);
        setTvLibraries(tvRes.libraries || []);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner" />
      </div>
    );
  }

  if (error) {
    return <div className="error-banner">{isAr ? 'فشل تحميل المكتبات:' : 'Failed to load libraries:'} {error}</div>;
  }

  return (
    <div className="library-landing">
      {/* Movie Libraries Section */}
      <div className="library-hero">
        <h1 className="library-hero-title">{isAr ? 'مكتبات الأفلام' : 'Movie Libraries'}</h1>
        <p className="library-hero-sub">
          {isAr ? 'اختر مكتبة أفلام لتصفح مجموعتها' : 'Choose a movie library to browse its collection'}
        </p>
      </div>
      <div className="library-grid">
        {libraries.map((lib) => (
          <button
            key={lib.id}
            className="library-card"
            id={`library-card-${lib.slug}`}
            onClick={() => onSelectLibrary(lib.slug)}
          >
            {lib.posters && lib.posters.length > 0 ? (
              <div className="library-card-backdrop">
                {lib.posters.map((poster, i) => (
                  <img
                    key={i}
                    src={poster}
                    className={`backdrop-poster-tile tile-${i}`}
                    alt=""
                    loading="lazy"
                  />
                ))}
              </div>
            ) : (
              <div className="library-card-backdrop empty" />
            )}
            <div className="library-card-overlay" />

            <div className="library-card-icon">📚</div>
            <h2 className="library-card-name">{translateLibraryName(lib.name, lang)}</h2>
            {lib.telegram_channel && (
              <div className="library-card-channel" title={lib.telegram_channel}>
                📡 {isAr ? 'قناة تيليجرام' : 'Telegram Channel'}
              </div>
            )}
            <div className="library-card-arrow">{isAr ? '←' : '→'}</div>
          </button>
        ))}
      </div>

      {/* TV Series Libraries Section */}
      <div className="library-hero" style={{ marginTop: '4rem' }}>
        <h1 className="library-hero-title">{isAr ? 'مكتبات المسلسلات' : 'TV Series Libraries'}</h1>
        <p className="library-hero-sub">
          {isAr ? 'اختر مكتبة مسلسلات لتصفح مجموعتها' : 'Choose a TV series library to browse its collection'}
        </p>
      </div>
      <div className="library-grid">
        {tvLibraries.map((lib) => (
          <button
            key={lib.id}
            className="library-card series-entry-card"
            id={`tv-library-card-${lib.slug}`}
            onClick={() => (onSelectTVLibrary ? onSelectTVLibrary(lib.slug) : onSelectLibrary(`tv/${lib.slug}`))}
          >
            {lib.posters && lib.posters.length > 0 ? (
              <div className="library-card-backdrop">
                {lib.posters.map((poster, i) => (
                  <img
                    key={i}
                    src={poster}
                    className={`backdrop-poster-tile tile-${i}`}
                    alt=""
                    loading="lazy"
                  />
                ))}
              </div>
            ) : (
              <div className="library-card-backdrop series-backdrop">
                <div className="series-backdrop-gradient" />
              </div>
            )}
            <div className="library-card-overlay" />

            <div className="library-card-icon">📺</div>
            <h2 className="library-card-name">{translateLibraryName(lib.name, lang)}</h2>
            {lib.telegram_channel && (
              <div className="library-card-channel" title={lib.telegram_channel}>
                📡 {isAr ? 'قناة تيليجرام' : 'Telegram Channel'}
              </div>
            )}
            <div className="library-card-arrow">{isAr ? '←' : '→'}</div>
          </button>
        ))}

        {tvLibraries.length === 0 && (
          <div className="empty-state" style={{ gridColumn: '1 / -1', padding: '2rem' }}>
            <p>{isAr ? 'لا توجد مكتبات مسلسلات حالياً' : 'No TV series libraries found'}</p>
          </div>
        )}
      </div>

      {/* Featured & Trending TV Series Section */}
      <div style={{ marginTop: '5rem', paddingBottom: '2rem' }}>
        <FeaturedSeriesSection lang={lang} />
      </div>
    </div>
  );
}
