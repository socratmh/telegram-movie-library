import { useState, useEffect } from 'react';
import { fetchFeaturedTVSeries, formatImageUrl } from '../api/client';
import { translateLibraryName } from '../utils/translator';
import { formatTelegramUrl } from './TelegramBanner';

export default function FeaturedSeriesSection({ lang = 'en' }) {
  const [featuredItems, setFeaturedItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const isAr = lang === 'ar';

  useEffect(() => {
    fetchFeaturedTVSeries()
      .then((res) => {
        setFeaturedItems(res.items || []);
      })
      .catch((err) => {
        console.error('Failed to load featured TV series:', err);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading || featuredItems.length === 0) {
    return null;
  }

  return (
    <div className="featured-series-section">
      <div className="featured-section-header">
        <h2 className="featured-section-title">
          <span style={{ marginInlineEnd: '0.5rem' }}>🔥</span>
          {isAr ? 'مسلسلات مميزة وشائعة' : 'Featured & Trending Series'}
        </h2>
        <p className="featured-section-sub">
          {isAr
            ? 'تصفح أحدث وأكثر المسلسلات مشاهدة على تيليجرام'
            : 'Browse the latest and most popular series currently airing on Telegram'}
        </p>
      </div>

      <div className="featured-series-grid">
        {featuredItems.map((item) => {
          const channelUrl = formatTelegramUrl(item.telegram_channel_link);
          const categoryText = isAr
            ? (item.category === 'Trending' ? 'شائع' : item.category === 'Popular' ? 'الأكثر مشاهدة' : item.category === 'Currently Airing' ? 'يعرض حالياً' : item.category)
            : item.category;

          return (
            <div key={item.id} className="featured-card">
              <div className="featured-card-poster-wrap">
                {item.poster_url ? (
                  <img
                    src={formatImageUrl(item.poster_url)}
                    alt={item.title}
                    className="featured-card-poster"
                    loading="lazy"
                  />
                ) : (
                  <div className="movie-card-no-poster">
                    <span className="no-poster-text">{item.title}</span>
                  </div>
                )}
                {categoryText && (
                  <div className="featured-category-badge">
                    ⚡ {categoryText}
                  </div>
                )}
              </div>

              <div className="featured-card-content">
                <h3 className="featured-card-title">
                  {translateLibraryName(item.title, lang)}
                </h3>
                {item.description && (
                  <p className="featured-card-desc">{item.description}</p>
                )}
                <a
                  href={channelUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="featured-watch-btn"
                >
                  <span>🚀</span>
                  <span>{isAr ? 'شاهد على تيليجرام' : 'Watch on Telegram'}</span>
                </a>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
