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
  'TV Movie': 'فيلم تلفزيوني',
  'Thriller': 'إثارة',
  'War': 'حرب',
  'War & Politics': 'حرب وسياسة',
  'Western': 'غربي'
};

export default function GenreFilter({ genres, activeGenre, onToggle, lang = 'en' }) {
  if (!genres || genres.length === 0) return null;

  const isAr = lang === 'ar';

  return (
    <div className="genre-filter" id="genre-filter">
      <button
        className={`genre-tag ${!activeGenre ? 'active' : ''}`}
        onClick={() => onToggle('')}
        type="button"
      >
        {isAr ? 'الكل' : 'All'}
      </button>
      {genres.map((g) => (
        <button
          key={g}
          className={`genre-tag ${activeGenre === g ? 'active' : ''}`}
          onClick={() => onToggle(g)}
          type="button"
        >
          {isAr ? (GENRE_MAP[g] || g) : g}
        </button>
      ))}
    </div>
  );
}
