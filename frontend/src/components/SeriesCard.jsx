export default function SeriesCard({ series, onClick, lang = 'en' }) {
  const isAr = lang === 'ar';
  const rating = series.vote_average != null ? series.vote_average.toFixed(1) : null;
  const year = series.first_air_date ? series.first_air_date.slice(0, 4) : null;

  return (
    <div
      className="movie-card series-card"
      onClick={() => onClick(series.id)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick(series.id)}
      id={`series-card-${series.id}`}
    >
      {series.poster_url ? (
        <img
          className="movie-card-poster"
          src={series.poster_url}
          alt={series.title}
          loading="lazy"
        />
      ) : (
        <div className="movie-card-no-poster" aria-label={isAr ? 'الملصق غير متوفر' : 'No poster available'}>
          <span className="no-poster-text">{series.title}</span>
        </div>
      )}

      {rating && (
        <div className="movie-card-rating-badge">
          ★ {rating}
        </div>
      )}

      <div className="movie-card-overlay">
        <div className="movie-card-title">{series.title}</div>
        <div className="movie-card-meta">
          {rating && <span className="movie-card-rating">★ {rating}</span>}
          {year && <span className="movie-card-year">{year}</span>}
          {series.number_of_seasons && (
            <span>{series.number_of_seasons} {isAr ? 'مواسم' : (series.number_of_seasons === 1 ? 'Season' : 'Seasons')}</span>
          )}
        </div>
      </div>
    </div>
  );
}
