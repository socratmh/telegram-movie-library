import React from 'react';

export default function FloatingBackButton({ onClick, lang = 'en' }) {
  const isAr = lang === 'ar';
  
  return (
    <button 
      className={`floating-back-btn ${isAr ? 'rtl' : 'ltr'}`} 
      onClick={onClick}
      title={isAr ? 'رجوع' : 'Back'}
    >
      <span className="floating-back-icon">{isAr ? '←' : '←'}</span>
      <span className="floating-back-text">{isAr ? 'رجوع' : 'Back'}</span>
    </button>
  );
}
