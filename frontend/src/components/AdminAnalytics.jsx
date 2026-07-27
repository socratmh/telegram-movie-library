import { useState, useEffect, useCallback } from 'react';
import {
  adminFetchAnalyticsSummary,
  adminFetchAnalyticsVisitors,
  adminFetchAnalyticsBreakdown,
  adminFetchAnalyticsCharts,
} from '../api/client';

// ---------------------------------------------------------------------------
// Mini bar chart (pure CSS/HTML)
// ---------------------------------------------------------------------------
function BarChart({ data, title, color = '#a78bfa' }) {
  if (!data || data.length === 0) return null;
  const max = Math.max(...data.map((d) => d.count), 1);

  return (
    <div className="analytics-chart-card">
      <h3 className="analytics-chart-title">{title}</h3>
      <div className="analytics-bar-chart">
        {data.map((d, i) => (
          <div key={i} className="analytics-bar-col" title={`${d.label}: ${d.count}`}>
            <div
              className="analytics-bar"
              style={{
                height: `${(d.count / max) * 100}%`,
                background: color,
              }}
            />
            <span className="analytics-bar-label">
              {d.label?.length > 5 ? d.label.slice(5) : d.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Breakdown table
// ---------------------------------------------------------------------------
function BreakdownTable({ data, title, icon }) {
  if (!data || data.length === 0) return null;
  const total = data.reduce((s, d) => s + d.count, 0);

  return (
    <div className="analytics-breakdown-card">
      <h3 className="analytics-breakdown-title">{icon} {title}</h3>
      <div className="analytics-breakdown-list">
        {data.map((item, i) => {
          const pct = total > 0 ? ((item.count / total) * 100).toFixed(1) : 0;
          return (
            <div key={i} className="analytics-breakdown-row">
              <span className="analytics-breakdown-label">{item.label}</span>
              <div className="analytics-breakdown-bar-wrap">
                <div
                  className="analytics-breakdown-bar-fill"
                  style={{ width: `${pct}%` }}
                />
              </div>
              <span className="analytics-breakdown-count">{item.count}</span>
              <span className="analytics-breakdown-pct">{pct}%</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main analytics component
// ---------------------------------------------------------------------------
export default function AdminAnalytics({ lang = 'en' }) {
  const isAr = lang === 'ar';
  const [summary, setSummary] = useState(null);
  const [visitors, setVisitors] = useState(null);
  const [breakdown, setBreakdown] = useState(null);
  const [charts, setCharts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [visitorPage, setVisitorPage] = useState(1);
  const [subTab, setSubTab] = useState('overview');

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [sumRes, brkRes, chtRes] = await Promise.all([
        adminFetchAnalyticsSummary(),
        adminFetchAnalyticsBreakdown(),
        adminFetchAnalyticsCharts(),
      ]);
      setSummary(sumRes);
      setBreakdown(brkRes);
      setCharts(chtRes);
    } catch (err) {
      console.error('Analytics load error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const loadVisitors = useCallback(async (pg = 1) => {
    try {
      const res = await adminFetchAnalyticsVisitors({ page: pg, pageSize: 30 });
      setVisitors(res);
      setVisitorPage(pg);
    } catch (err) {
      console.error('Visitors load error:', err);
    }
  }, []);

  useEffect(() => {
    loadData();
    loadVisitors(1);
  }, [loadData, loadVisitors]);

  if (loading && !summary) {
    return (
      <div className="loading-spinner" style={{ padding: '3rem' }}>
        <div className="spinner" />
      </div>
    );
  }

  return (
    <div className="analytics-container">
      {/* Sub-tabs */}
      <div className="analytics-subtabs">
        <button
          className={`analytics-subtab ${subTab === 'overview' ? 'active' : ''}`}
          onClick={() => setSubTab('overview')}
        >
          {isAr ? '📊 نظرة عامة' : '📊 Overview'}
        </button>
        <button
          className={`analytics-subtab ${subTab === 'visitors' ? 'active' : ''}`}
          onClick={() => { setSubTab('visitors'); loadVisitors(1); }}
        >
          {isAr ? '👥 الزوار' : '👥 Visitors'}
        </button>
        <button
          className={`analytics-subtab ${subTab === 'breakdown' ? 'active' : ''}`}
          onClick={() => setSubTab('breakdown')}
        >
          {isAr ? '📈 تفاصيل' : '📈 Breakdown'}
        </button>
      </div>

      {/* ---- OVERVIEW TAB ---- */}
      {subTab === 'overview' && summary && (
        <>
          {/* Summary cards */}
          <div className="analytics-summary-grid">
            <div className="analytics-stat-card">
              <div className="analytics-stat-value">{summary.total_visits}</div>
              <div className="analytics-stat-label">{isAr ? 'إجمالي الزيارات' : 'Total Visits'}</div>
            </div>
            <div className="analytics-stat-card">
              <div className="analytics-stat-value">{summary.unique_visitors}</div>
              <div className="analytics-stat-label">{isAr ? 'زوار فريدون' : 'Unique Visitors'}</div>
            </div>
            <div className="analytics-stat-card accent">
              <div className="analytics-stat-value">{summary.active_today}</div>
              <div className="analytics-stat-label">{isAr ? 'نشطون اليوم' : 'Active Today'}</div>
            </div>
            <div className="analytics-stat-card">
              <div className="analytics-stat-value">{summary.active_this_week}</div>
              <div className="analytics-stat-label">{isAr ? 'هذا الأسبوع' : 'This Week'}</div>
            </div>
            <div className="analytics-stat-card">
              <div className="analytics-stat-value">{summary.active_this_month}</div>
              <div className="analytics-stat-label">{isAr ? 'هذا الشهر' : 'This Month'}</div>
            </div>
          </div>

          {/* Charts */}
          {charts && (
            <div className="analytics-charts-row">
              <BarChart
                data={charts.daily}
                title={isAr ? 'الزيارات اليومية (آخر 30 يوم)' : 'Daily Visits (Last 30 Days)'}
                color="#a78bfa"
              />
              <BarChart
                data={charts.monthly}
                title={isAr ? 'الزيارات الشهرية' : 'Monthly Visits'}
                color="#38bdf8"
              />
            </div>
          )}

          {/* Quick breakdowns */}
          {breakdown && (
            <div className="analytics-breakdown-grid">
              <BreakdownTable data={breakdown.by_country} title={isAr ? 'حسب البلد' : 'By Country'} icon="🌍" />
              <BreakdownTable data={breakdown.by_device} title={isAr ? 'حسب الجهاز' : 'By Device'} icon="📱" />
            </div>
          )}
        </>
      )}

      {/* ---- VISITORS TAB ---- */}
      {subTab === 'visitors' && visitors && (
        <div className="analytics-visitors-section">
          <div className="analytics-visitors-header">
            <span>{isAr ? `${visitors.total} زيارة` : `${visitors.total} visits`}</span>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
              {isAr ? `صفحة ${visitors.page} / ${visitors.total_pages}` : `Page ${visitors.page} / ${visitors.total_pages}`}
            </span>
          </div>
          <div className="admin-table-wrap">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>{isAr ? 'التاريخ' : 'Date'}</th>
                  <th>{isAr ? 'البلد' : 'Country'}</th>
                  <th>{isAr ? 'المدينة' : 'City'}</th>
                  <th>{isAr ? 'الجهاز' : 'Device'}</th>
                  <th>{isAr ? 'النظام' : 'OS'}</th>
                  <th>{isAr ? 'المتصفح' : 'Browser'}</th>
                  <th>IP</th>
                  <th>{isAr ? 'المصدر' : 'Referrer'}</th>
                  <th>{isAr ? 'الصفحة' : 'Page'}</th>
                </tr>
              </thead>
              <tbody>
                {visitors.items.map((v) => (
                  <tr key={v.id}>
                    <td style={{ whiteSpace: 'nowrap', fontSize: '0.8rem' }}>
                      {v.created_at ? new Date(v.created_at).toLocaleString() : '-'}
                    </td>
                    <td>{v.country || '-'}</td>
                    <td>{v.city || '-'}</td>
                    <td>{v.device_type || '-'}</td>
                    <td>{v.os || '-'}</td>
                    <td>{v.browser || '-'}</td>
                    <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{v.ip_address || '-'}</td>
                    <td>{v.referrer || '-'}</td>
                    <td style={{ maxWidth: '150px', overflow: 'hidden', textOverflow: 'ellipsis' }}>{v.page_path || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {visitors.total_pages > 1 && (
            <div className="analytics-pagination">
              <button
                className="admin-btn"
                disabled={visitorPage <= 1}
                onClick={() => loadVisitors(visitorPage - 1)}
              >
                {isAr ? 'السابق' : 'Prev'}
              </button>
              <span>{visitorPage} / {visitors.total_pages}</span>
              <button
                className="admin-btn"
                disabled={visitorPage >= visitors.total_pages}
                onClick={() => loadVisitors(visitorPage + 1)}
              >
                {isAr ? 'التالي' : 'Next'}
              </button>
            </div>
          )}
        </div>
      )}

      {/* ---- BREAKDOWN TAB ---- */}
      {subTab === 'breakdown' && breakdown && (
        <div className="analytics-breakdown-grid full">
          <BreakdownTable data={breakdown.by_country} title={isAr ? 'حسب البلد' : 'By Country'} icon="🌍" />
          <BreakdownTable data={breakdown.by_device} title={isAr ? 'حسب الجهاز' : 'By Device'} icon="📱" />
          <BreakdownTable data={breakdown.by_os} title={isAr ? 'حسب نظام التشغيل' : 'By OS'} icon="💻" />
          <BreakdownTable data={breakdown.by_browser} title={isAr ? 'حسب المتصفح' : 'By Browser'} icon="🌐" />
          <BreakdownTable data={breakdown.top_pages} title={isAr ? 'أكثر الصفحات زيارة' : 'Top Pages'} icon="📄" />
          <BreakdownTable data={breakdown.by_referrer} title={isAr ? 'حسب المصدر' : 'By Referrer'} icon="🔗" />
        </div>
      )}
    </div>
  );
}
