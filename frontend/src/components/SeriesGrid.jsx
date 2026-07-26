import SeriesCard from './SeriesCard';

export default function SeriesGrid({ series, loading, error, onSeriesClick, lang = 'en' }) {
  const isAr = lang === 'ar';

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner" />
      </div>
    );
  }

  if (error) {
    return <div className="error-banner">{isAr ? 'فشل تحميل المسلسلات:' : 'Failed to load series:'} {error}</div>;
  }

  if (!series || series.length === 0) {
    return (
      <div className="empty-state">
        <span className="empty-icon">📺</span>
        <p>{isAr ? 'لا توجد مسلسلات' : 'No series found'}</p>
      </div>
    );
  }

  return (
    <div className="movie-grid" id="series-grid">
      {series.map((s) => (
        <SeriesCard
          key={s.id}
          series={s}
          onClick={onSeriesClick}
          lang={lang}
        />
      ))}
    </div>
  );
}
