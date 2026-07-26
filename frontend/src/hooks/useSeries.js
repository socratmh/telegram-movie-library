import { useState, useEffect } from 'react';
import { fetchSeries, fetchSeriesGenres, fetchSeriesStats } from '../api/client';

export function useSeries(libraryId = null) {
  const [series, setSeries] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [genre, setGenre] = useState('');
  const [genres, setGenres] = useState([]);
  const [sortBy, setSortBy] = useState('title');
  const [sortOrder, setSortOrder] = useState('asc');
  const [stats, setStats] = useState(null);

  // Fetch genres
  useEffect(() => {
    fetchSeriesGenres({ libraryId })
      .then((data) => setGenres(data.genres || []))
      .catch(() => {});
  }, [libraryId]);

  // Fetch stats
  useEffect(() => {
    fetchSeriesStats({ libraryId })
      .then((data) => setStats(data))
      .catch(() => {});
  }, [libraryId]);

  // Reset page when filters change
  useEffect(() => {
    setPage(1);
  }, [search, genre, sortBy, sortOrder, libraryId]);

  // Fetch series
  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchSeries({ page, pageSize: 20, search, genre, sortBy, sortOrder, libraryId })
      .then((data) => {
        setSeries(data.items || []);
        setTotal(data.total || 0);
        setTotalPages(data.total_pages || 0);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [page, search, genre, sortBy, sortOrder, libraryId]);

  return {
    series,
    total,
    page,
    setPage,
    totalPages,
    loading,
    error,
    search,
    setSearch,
    genre,
    setGenre,
    genres,
    sortBy,
    setSortBy,
    sortOrder,
    setSortOrder,
    stats,
  };
}
