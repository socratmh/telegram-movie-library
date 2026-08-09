# Graph Report - Movis_with_Telegram  (2026-07-27)

## Corpus Check
- 98 files · ~53,815 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 768 nodes · 1406 edges · 72 communities (53 shown, 19 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 47 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b3571519`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_MovieQueries|MovieQueries]]
- [[_COMMUNITY_movies.py|movies.py]]
- [[_COMMUNITY_App.jsx|App.jsx]]
- [[_COMMUNITY_process_movie|process_movie]]
- [[_COMMUNITY_package.json|package.json]]
- [[_COMMUNITY_get_db_url|get_db_url]]
- [[_COMMUNITY_tmdb_service.py|tmdb_service.py]]
- [[_COMMUNITY_.oxlintrc.json|.oxlintrc.json]]
- [[_COMMUNITY_run.py|run.py]]
- [[_COMMUNITY_config.py|config.py]]
- [[_COMMUNITY__parse_genres|_parse_genres]]
- [[_COMMUNITY_Any|Any]]
- [[_COMMUNITY_Path|Path]]
- [[_COMMUNITY___init__.py|__init__.py]]
- [[_COMMUNITY_TaskManager|TaskManager]]
- [[_COMMUNITY_migrate_channel_links.py|migrate_channel_links.py]]
- [[_COMMUNITY_config.py|config.py]]
- [[_COMMUNITY__parse_genres|_parse_genres]]
- [[_COMMUNITY_MovieGrid.jsx|MovieGrid.jsx]]
- [[_COMMUNITY_admin.py|admin.py]]
- [[_COMMUNITY_MovieGrid.jsx|MovieGrid.jsx]]
- [[_COMMUNITY_StatsPanel.jsx|StatsPanel.jsx]]
- [[_COMMUNITY_GenreFilter.jsx|GenreFilter.jsx]]
- [[_COMMUNITY_SearchBar.jsx|SearchBar.jsx]]
- [[_COMMUNITY_adminAuth.js|adminAuth.js]]
- [[_COMMUNITY_Session|Session]]
- [[_COMMUNITY_Path|Path]]
- [[_COMMUNITY_config.py|config.py]]
- [[_COMMUNITY_Request|Request]]
- [[_COMMUNITY_Any|Any]]
- [[_COMMUNITY_Any|Any]]
- [[_COMMUNITY_Path|Path]]
- [[_COMMUNITY_TelegramClient|TelegramClient]]
- [[_COMMUNITY_analytics.py|analytics.py]]
- [[_COMMUNITY_GenreFilter.jsx|GenreFilter.jsx]]
- [[_COMMUNITY_Hero.jsx|Hero.jsx]]
- [[_COMMUNITY_SearchBar.jsx|SearchBar.jsx]]
- [[_COMMUNITY_process_series|process_series]]
- [[_COMMUNITY_adminAuth.js|adminAuth.js]]
- [[_COMMUNITY_Any|Any]]
- [[_COMMUNITY_config.py|config.py]]
- [[_COMMUNITY_GenreFilter.jsx|GenreFilter.jsx]]
- [[_COMMUNITY_Request|Request]]
- [[_COMMUNITY_LibraryUpdateRequest|LibraryUpdateRequest]]
- [[_COMMUNITY_Session|Session]]
- [[_COMMUNITY_Session|Session]]
- [[_COMMUNITY_TVLibraryCreateRequest|TVLibraryCreateRequest]]
- [[_COMMUNITY_TVLibraryUpdateRequest|TVLibraryUpdateRequest]]
- [[_COMMUNITY_BaseModel|BaseModel]]
- [[_COMMUNITY_migrate_tv_channel_links.py|migrate_tv_channel_links.py]]
- [[_COMMUNITY_admin_create_tv_library|admin_create_tv_library]]
- [[_COMMUNITY__parse_genres|_parse_genres]]
- [[_COMMUNITY__parse_genres|_parse_genres]]
- [[_COMMUNITY_admin_create_featured_tv|admin_create_featured_tv]]

## God Nodes (most connected - your core abstractions)
1. `SeriesQueries` - 24 edges
2. `request()` - 24 edges
3. `MovieQueries` - 22 edges
4. `Movie` - 17 edges
5. `mutate()` - 17 edges
6. `MovieDatabase` - 17 edges
7. `_get_session_factory()` - 16 edges
8. `Library` - 16 edges
9. `TaskManager` - 15 edges
10. `SeriesDatabase` - 15 edges

## Surprising Connections (you probably didn't know these)
- `admin_list_libraries()` --indirect_call--> `Library`  [INFERRED]
  backend/routers/admin.py → database/models.py
- `admin_list_libraries()` --indirect_call--> `Movie`  [INFERRED]
  backend/routers/admin.py → database/models.py
- `admin_update_library()` --indirect_call--> `Library`  [INFERRED]
  backend/routers/admin.py → database/models.py
- `admin_update_library()` --indirect_call--> `Movie`  [INFERRED]
  backend/routers/admin.py → database/models.py
- `admin_scan_library()` --indirect_call--> `Library`  [INFERRED]
  backend/routers/admin.py → database/models.py

## Import Cycles
- None detected.

## Communities (72 total, 19 thin omitted)

### Community 0 - "MovieQueries"
Cohesion: 0.18
Nodes (12): _clean_title(), extract_movie_title(), _extract_quality(), _is_valid_title(), parse_movie_message(), ParsedMovie, Extract a likely movie title and supported video quality from a Telegram message, MovieRecord (+4 more)

### Community 1 - "movies.py"
Cohesion: 0.06
Nodes (34): global_exception_handler(), Request, Health-check / welcome endpoint., root(), SecurityHeadersMiddleware, MovieQueries, Any, Session (+26 more)

### Community 2 - "App.jsx"
Cohesion: 0.06
Nodes (55): adminCancelTask(), adminCreateFeaturedTVSeries(), adminCreateLibrary(), adminCreateTVLibrary(), adminDeleteFeaturedTVSeries(), adminDeleteLibrary(), adminDeleteTVLibrary(), adminFetchAnalyticsBreakdown() (+47 more)

### Community 3 - "process_movie"
Cohesion: 0.06
Nodes (49): admin_delete_library(), admin_upload_image(), Delete a library and all associated movies/messages., Upload a custom image/poster file and return the access URL., Base, _path_env(), Settings, get_db_url() (+41 more)

### Community 4 - "package.json"
Cohesion: 0.13
Nodes (14): dependencies, react, react-dom, devDependencies, vite, @vitejs/plugin-react, name, private (+6 more)

### Community 5 - "get_db_url"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 6 - "tmdb_service.py"
Cohesion: 0.17
Nodes (10): caveman, Example output, How to invoke, See also, What it does, Auto-Clarity, Boundaries, Intensity (+2 more)

### Community 7 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 14 - "config.py"
Cohesion: 0.22
Nodes (6): _get_queries(), Request, Any, Session, Read-only query layer for TV series and libraries., SeriesQueries

### Community 15 - "_parse_genres"
Cohesion: 0.20
Nodes (9): Database Schema, File Purposes, Notes, Project Structure, Run, Setup, Telegram Movies, Test TMDB (+1 more)

### Community 16 - "Any"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 17 - "Path"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 19 - "TaskManager"
Cohesion: 0.13
Nodes (14): task_manager.py — In-memory background task manager.  Spawns CLI scripts (main.p, Launch update_tmdb.py for a specific library., Launch migrate_channel_links.py for a specific library., Launch migrate_tv_channel_links.py for a specific TV library., Launch main_tv.py scraper for a specific TV library., Launch update_tmdb_tv.py for a specific TV library., Manages background subprocess tasks with log capture., Launch main.py scraper for a specific library. (+6 more)

### Community 20 - "migrate_channel_links.py"
Cohesion: 0.43
Nodes (3): OnboardingModal(), formatTelegramUrl(), TelegramBanner()

### Community 21 - "config.py"
Cohesion: 0.18
Nodes (3): App(), AdminDashboard(), LibraryGrid()

### Community 22 - "_parse_genres"
Cohesion: 0.10
Nodes (36): AdminInfoResponse, block_refresh_token(), check_rate_limit(), create_access_token(), create_refresh_token(), decode_token(), get_current_admin(), is_refresh_blocked() (+28 more)

### Community 23 - "MovieGrid.jsx"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 24 - "admin.py"
Cohesion: 0.50
Nodes (3): For git commit hook, For native AGENTS.md integration, graphify reference: commit hook and native AGENTS.md integration

### Community 25 - "MovieGrid.jsx"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 26 - "StatsPanel.jsx"
Cohesion: 0.50
Nodes (3): Expanding the Oxlint configuration, React Compiler, React + Vite

### Community 39 - "config.py"
Cohesion: 0.22
Nodes (9): get_app_env(), get_database_path(), get_database_url(), get_telegram_channel_id(), Path, Return the current application environment (development | production)., Resolve the database path from the environment.      Keeps the backend indepen, Get the database URL from the environment for SQLAlchemy.      Only returns th (+1 more)

### Community 40 - "Request"
Cohesion: 0.12
Nodes (39): LibraryDetailResponse, TaskResponse, admin_cancel_task(), admin_create_library(), admin_delete_featured_tv(), admin_delete_tv_library(), admin_get_task(), admin_get_task_logs() (+31 more)

### Community 42 - "Any"
Cohesion: 0.10
Nodes (22): TMDB metadata for a TV series., A TV series scraped from a Telegram channel., TMDBTVSeries, TVSeries, Session, Link a TV series to its TMDB entry., SQLAlchemy repository for storing scraped TV series records., Return set of series titles stored for current library. (+14 more)

### Community 45 - "analytics.py"
Cohesion: 0.19
Nodes (23): analytics_breakdown(), analytics_charts(), analytics_summary(), analytics_visitors(), AnalyticsSummary, BreakdownItem, BreakdownResponse, ChartPoint (+15 more)

### Community 46 - "GenreFilter.jsx"
Cohesion: 0.12
Nodes (24): admin_list_featured_tv(), Return all manually managed featured TV series entries., get_series(), get_tv_library(), list_featured_tv(), list_series(), list_series_genres(), list_tv_libraries() (+16 more)

### Community 50 - "SearchBar.jsx"
Cohesion: 0.12
Nodes (18): main(), export_session_string.py — Helper script to export your local Telethon session a, Return a console-safe version of *text* (handles Windows cp1252)., run(), _safe(), Message, _clean_title(), _is_valid_title() (+10 more)

### Community 52 - "process_series"
Cohesion: 0.10
Nodes (25): Any, Lock, main(), build_poster_url(), _choose_best_match(), get_movie_details(), _normalize_title(), Search TMDB by movie title and return the best matching result.      Returned (+17 more)

### Community 53 - "adminAuth.js"
Cohesion: 0.26
Nodes (14): decodeTokenPayload(), getAccessToken(), getAuthHeaders(), getAuthHeadersAsync(), getRefreshToken(), getUsername(), isAuthenticated(), isTokenExpired() (+6 more)

### Community 55 - "config.py"
Cohesion: 0.40
Nodes (3): AR_TO_EN_WORDS, DIRECTORY_MAP, EN_TO_AR_WORDS

### Community 65 - "BaseModel"
Cohesion: 0.20
Nodes (16): LibraryCreateRequest, LibraryListResponse, LibraryUpdateRequest, MigrationRequest, MovieDetailResponse, MovieListItem, PaginatedResponse, Body for launching a channel scan. (+8 more)

### Community 66 - "migrate_tv_channel_links.py"
Cohesion: 0.24
Nodes (12): build_match_indexes(), _build_telegram_url(), main(), match_message(), MatchResult, migrate_tv(), MigrationStats, migrate_tv_channel_links.py — Migrate TV series Telegram links to a new channel. (+4 more)

### Community 67 - "admin_create_tv_library"
Cohesion: 0.22
Nodes (9): admin_create_tv_library(), admin_list_tv_libraries(), admin_update_tv_library(), List ALL TV libraries with detailed stats., Create a new TV series library., Update TV series library details., TVLibraryCreateRequest, TVLibraryDetailResponse (+1 more)

### Community 68 - "_parse_genres"
Cohesion: 0.32
Nodes (4): _parse_genres(), Any, Accept a JSON string or a plain list and always return ``list[str]``., TmdbMovieResponse

### Community 69 - "_parse_genres"
Cohesion: 0.32
Nodes (4): _parse_genres(), Any, Accept a JSON string or a plain list and always return ``list[str]``., TmdbTVResponse

### Community 70 - "admin_create_featured_tv"
Cohesion: 0.29
Nodes (7): admin_create_featured_tv(), admin_update_featured_tv(), Create a new manually managed featured TV series entry., Update an existing featured TV series entry., FeaturedTVCreateRequest, FeaturedTVResponse, FeaturedTVUpdateRequest

## Knowledge Gaps
- **84 isolated node(s):** `GENRE_MAP`, `GENRE_MAP`, `STATUS_MAP`, `GENRE_MAP`, `DIRECTORY_MAP` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeriesQueries` connect `config.py` to `movies.py`, `GenreFilter.jsx`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **What connects `Read-only query layer that powers the FastAPI endpoints.      Uses SQLAlchemy.`, `Accept a JSON string or a plain list and always return ``list[str]``.`, `Body for launching a channel scan.` to the rest of the system?**
  _207 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `movies.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06448979591836734 - nodes in this community are weakly interconnected._
- **Should `App.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.05712050078247261 - nodes in this community are weakly interconnected._
- **Should `process_movie` be split into smaller, more focused modules?**
  _Cohesion score 0.06202435312024353 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `get_db_url` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._