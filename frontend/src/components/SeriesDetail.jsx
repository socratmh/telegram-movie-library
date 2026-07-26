import { useState, useEffect } from 'react';
import { fetchSeriesDetail } from '../api/client';

const GENRE_MAP = {
  'Action': 'أكشن',
  'Action & Adventure': 'أكشن ومغامرة',
  'Adventure': 'مغامرة',
  'Animation': 'رسوم متحركة',
  'Comedy': 'كوميديا',
  'Crime': 'جريمة',
  'Documentary': 'وثائقي',
  'Drama': 'دراما',
  'Family': 'عائلي',
  'Fantasy': 'خيال',
  'History': 'تاريخ',
  'Horror': 'رعب',
  'Kids': 'أطفال',
  'Music': 'موسيقى',
  'Mystery': 'غموض',
  'News': 'أخبار',
  'Reality': 'واقعي',
  'Romance': 'رومانسية',
  'Sci-Fi & Fantasy': 'خيال علمي وخيال',
  'Science Fiction': 'خيال علمي',
  'Soap': 'مسلسل درامي',
  'Talk': 'حوار',
  'Thriller': 'إثارة',
  'War': 'حرب',
  'War & Politics': 'حرب وسياسة',
  'Western': 'غربي',
};

const STATUS_MAP = {
  'Returning Series': 'مستمر',
  'Ended': 'منتهي',
  'Canceled': 'ملغى',
  'In Production': 'قيد الإنتاج',
  'Planned': 'مخطط له',
  'Pilot': 'حلقة تجريبية',
};

export default function SeriesDetail({ seriesId, onClose, lang = 'en' }) {
  const [series, setSeries] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const isAr = lang === 'ar';

  useEffect(() => {
    if (!seriesId) return;
    setLoading(true);
    setError(null);

    fetchSeriesDetail(seriesId, { language: lang })
      .then((data) => setSeries(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [seriesId, lang]);

  // Close on Escape key
  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose]);

  // Prevent body scroll
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = ''; };
  }, []);

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onClose();
  };

  const tmdb = series?.tmdb;
  const rating = tmdb?.vote_average != null ? tmdb.vote_average.toFixed(1) : null;
  const year = tmdb?.first_air_date ? tmdb.first_air_date.slice(0, 4) : null;

  return (
    <div className={`modal-overlay ${isAr ? 'rtl' : 'ltr'}`} onClick={handleOverlayClick} id="series-detail-modal">
      <div className="modal-content" role="dialog" aria-label={isAr ? 'تفاصيل المسلسل' : 'Series details'}>
        <button className="modal-close" onClick={onClose} aria-label={isAr ? 'إغلاق' : 'Close'}>✕</button>

        {loading && (
          <div className="loading-spinner" style={{ padding: '4rem' }}>
            <div className="spinner" />
          </div>
        )}

        {error && <div className="error-banner" style={{ margin: '2rem' }}>⚠ {error}</div>}

        {series && !loading && (
          <>
            {tmdb?.backdrop_url ? (
              <img className="modal-backdrop-img" src={tmdb.backdrop_url} alt="" />
            ) : (
              <div className="modal-backdrop-placeholder" />
            )}

            <div className="modal-body" style={{ direction: isAr ? 'rtl' : 'ltr' }}>
              {/* Poster */}
              {tmdb?.poster_url ? (
                <img className="modal-poster" src={tmdb.poster_url} alt={series.title} />
              ) : (
                <div className="modal-poster-placeholder">📺</div>
              )}

              {/* Info */}
              <div className="modal-info">
                <h1 className="modal-title">{series.title}</h1>

                {tmdb?.original_name && tmdb.original_name !== series.title && (
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '0.5rem', fontStyle: 'italic' }}>
                    {tmdb.original_name}
                  </div>
                )}

                <div className="modal-meta">
                  {rating && (
                    <span className="modal-rating">★ {rating}</span>
                  )}
                  {year && <span>{year}</span>}
                  {tmdb?.number_of_seasons && (
                    <span>{tmdb.number_of_seasons} {isAr ? 'مواسم' : (tmdb.number_of_seasons === 1 ? 'Season' : 'Seasons')}</span>
                  )}
                  {tmdb?.number_of_episodes && (
                    <span>{tmdb.number_of_episodes} {isAr ? 'حلقة' : 'Ep'}</span>
                  )}
                  {tmdb?.status && (
                    <span className="series-status-badge">
                      {isAr ? (STATUS_MAP[tmdb.status] || tmdb.status) : tmdb.status}
                    </span>
                  )}
                </div>

                {tmdb?.genres && tmdb.genres.length > 0 && (
                  <div className="modal-genres">
                    {tmdb.genres.map((g) => (
                      <span className="modal-genre-tag" key={g}>{isAr ? (GENRE_MAP[g] || g) : g}</span>
                    ))}
                  </div>
                )}

                {tmdb?.overview && (
                  <p className="modal-overview">{tmdb.overview}</p>
                )}

                {series.telegram_channel_link && (
                  <a
                    className="telegram-watch-btn series-channel-btn"
                    href={series.telegram_channel_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    id="open-series-channel-btn"
                  >
                    {isAr ? '📺 افتح قناة المسلسل' : '📺 Open Series Channel'}
                  </a>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
