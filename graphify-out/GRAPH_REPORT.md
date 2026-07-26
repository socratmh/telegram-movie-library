# Graph Report - Movis_with_Telegram  (2026-07-26)

## Corpus Check
- 90 files · ~41,118 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 691 nodes · 1250 edges · 55 communities (40 shown, 15 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 31 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3cbb7dc3`
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
- [[_COMMUNITY_MovieGrid.jsx|MovieGrid.jsx]]
- [[_COMMUNITY_GenreFilter.jsx|GenreFilter.jsx]]
- [[_COMMUNITY_Hero.jsx|Hero.jsx]]
- [[_COMMUNITY_SearchBar.jsx|SearchBar.jsx]]
- [[_COMMUNITY_process_series|process_series]]
- [[_COMMUNITY_adminAuth.js|adminAuth.js]]
- [[_COMMUNITY_Any|Any]]

## God Nodes (most connected - your core abstractions)
1. `MovieQueries` - 22 edges
2. `SeriesQueries` - 20 edges
3. `TaskManager` - 19 edges
4. `request()` - 18 edges
5. `MovieDatabase` - 17 edges
6. `_get_session_factory()` - 16 edges
7. `SeriesDatabase` - 15 edges
8. `process_series()` - 15 edges
9. `process_movie()` - 15 edges
10. `mutate()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `run()` --calls--> `SeriesDatabase`  [EXTRACTED]
  main_tv.py → scraper/tv_database.py
- `migrate()` --indirect_call--> `Library`  [INFERRED]
  migrate_channel_links.py → database/models.py
- `main()` --indirect_call--> `Library`  [INFERRED]
  migrate_to_postgres.py → database/models.py
- `build_match_indexes()` --indirect_call--> `TMDBMovie`  [INFERRED]
  migrate_channel_links.py → database/models.py
- `main()` --indirect_call--> `TMDBMovie`  [INFERRED]
  migrate_to_postgres.py → database/models.py

## Import Cycles
- None detected.

## Communities (55 total, 15 thin omitted)

### Community 0 - "MovieQueries"
Cohesion: 0.11
Nodes (32): Base, get_db_url(), init_db(), Library, Movie, Helper to determine the database URL, Initializes the database and returns the sessionmaker., TelegramMessage (+24 more)

### Community 1 - "movies.py"
Cohesion: 0.06
Nodes (46): Any, MovieQueries, Read-only query layer that powers the FastAPI endpoints.      Uses SQLAlchemy., GenreListResponse, LibraryCreateRequest, LibraryDetailResponse, LibraryListResponse, LibraryResponse (+38 more)

### Community 2 - "App.jsx"
Cohesion: 0.07
Nodes (57): adminCancelTask(), adminCreateLibrary(), adminCreateTVLibrary(), adminDeleteLibrary(), adminDeleteTVLibrary(), adminFetchLibraries(), adminFetchTask(), adminFetchTaskLogs() (+49 more)

### Community 3 - "process_movie"
Cohesion: 0.12
Nodes (19): Lock, main(), build_poster_url(), _choose_best_match(), get_movie_details(), _normalize_title(), Search TMDB by movie title and return the best matching result.      Returned, Fetch detailed TMDB metadata for a movie.      Returned keys:     - poster_pa (+11 more)

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
Cohesion: 0.12
Nodes (20): Return a console-safe version of *text* (handles Windows cp1252)., run(), _safe(), Message, _clean_title(), extract_movie_title(), _extract_quality(), _is_valid_title() (+12 more)

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
Cohesion: 0.09
Nodes (45): admin_cancel_task(), admin_create_library(), admin_create_tv_library(), admin_delete_library(), admin_delete_tv_library(), admin_get_task(), admin_get_task_logs(), admin_list_libraries() (+37 more)

### Community 46 - "GenreFilter.jsx"
Cohesion: 0.05
Nodes (51): global_exception_handler(), Request, Health-check / welcome endpoint., root(), SecurityHeadersMiddleware, _get_queries(), get_series(), get_tv_library() (+43 more)

### Community 50 - "SearchBar.jsx"
Cohesion: 0.06
Nodes (33): _path_env(), Settings, main(), export_session_string.py — Helper script to export your local Telethon session a, fix_message_id_constraint.py — One-time schema migration.  Removes the old UNIQU, Return a console-safe version of *text* (handles Windows cp1252)., run(), _safe() (+25 more)

### Community 52 - "process_series"
Cohesion: 0.11
Nodes (18): Session, Link a TV series to its TMDB entry., SQLAlchemy repository for storing scraped TV series records., Return set of series titles stored for current library., Find or create a TV series by title. Returns the series ID., Bulk-save series records. Returns count of newly created entries., Return series in current library that don't have TMDB data., Save TMDB TV metadata. Returns the tmdb_tv_series row ID. (+10 more)

### Community 53 - "adminAuth.js"
Cohesion: 0.26
Nodes (14): decodeTokenPayload(), getAccessToken(), getAuthHeaders(), getAuthHeadersAsync(), getRefreshToken(), getUsername(), isAuthenticated(), isTokenExpired() (+6 more)

## Knowledge Gaps
- **84 isolated node(s):** `GENRE_MAP`, `GENRE_MAP`, `STATUS_MAP`, `DIRECTORY_MAP`, `AR_TO_EN_WORDS` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TaskManager` connect `TaskManager` to `Request`, `GenreFilter.jsx`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **What connects `Admin API router — library CRUD, task management, and background operations.`, `List ALL libraries with detailed stats (including inactive).`, `Create a new library.` to the rest of the system?**
  _197 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MovieQueries` be split into smaller, more focused modules?**
  _Cohesion score 0.1091581868640148 - nodes in this community are weakly interconnected._
- **Should `movies.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06093189964157706 - nodes in this community are weakly interconnected._
- **Should `App.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.07203219315895372 - nodes in this community are weakly interconnected._
- **Should `process_movie` be split into smaller, more focused modules?**
  _Cohesion score 0.12310606060606061 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._