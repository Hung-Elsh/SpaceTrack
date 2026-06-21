Space Track project

### The target:

- A map of tracked objects in orbit: A 3D globe and a 2D static map of tracked objects in orbit (satellites, asteroids,
  debris, ...)
- Data is updated daily and can also be used to build historical maps.
- Users can filter by object type, country of origin, orbit type (LEO/MEO/GEO), and launch date range.
- Clicking an object shows its detail: name, NORAD ID, TLE data, orbital parameters, country, launch date.

---

### Project Structure:

1. **Source data** — www.space-track.org (requires free account; provides TLE and catalog data via REST API)
2. **AWS S3 Bucket** — stores raw JSON/CSV responses from the API; partitioned by date (`/raw/YYYY/MM/DD/`)
3. **AWS Lambda** — daily scheduled pull (EventBridge Scheduler) that fetches new data and writes to S3
4. **Airflow** — orchestrates the full pipeline: extract → validate → transform → load; handles retries and alerting
5. **Postgres Data Warehouse** — stores normalized, transformed orbital data and app configuration (object metadata,
   filter presets)
6. **Snowflake** — long-term historical storage and analytical queries (trend analysis, debris growth over time)
7. **Python Flask API** — serves object data to the frontend; endpoints for current snapshot, historical date, object
   detail, and filter queries
8. **Report UI** — frontend with 3D globe (CesiumJS or Three.js) and 2D map (Leaflet or Mapbox); filter panel, object
   detail sidebar

---

### Data Model (core tables):

**tracked_objects**

- `norad_id` (PK), `name`, `object_type` (PAYLOAD / ROCKET_BODY / DEBRIS / UNKNOWN)
- `country_code`, `launch_date`, `decay_date`, `status`

**orbital_snapshots**

- `norad_id` (FK), `snapshot_date`, `tle_line1`, `tle_line2`
- `inclination`, `eccentricity`, `apogee_km`, `perigee_km`, `period_min`, `raan`, `arg_of_perigee`
- `lat`, `lon`, `altitude_km` (computed from TLE at snapshot time using `sgp4` library)

**pipeline_runs**

- `run_id`, `run_date`, `source_name`, `status`, `records_fetched`, `records_loaded`, `error_message`

---

### Phase 1: Build the UI

**Target:** A working map that renders dummy/static data so the visual layer is validated before real data is wired in.

Tasks:

- [x] Set up frontend project (HTML + JS)
- [x] Integrate 3D globe (CesiumJS free tier or Three.js + globe.gl)
- [x] Integrate 2D map (Leaflet.js)
- [ ] Render 50–100 dummy satellite points with name + orbit type
- [x] Add basic filter panel (object type toggle, orbit altitude slider)
- [x] Add object detail panel on click (name, NORAD ID, altitude, country)
- [x] Toggle between 3D globe and 2D flat map views

**Tech choices to decide:** CesiumJS (rich but heavier) vs. globe.gl (lighter, Three.js-based)

---

### Phase 2: Build Data Structure

**Target:** Define and create all storage layers; populate with a real historical snapshot.

Tasks:

- [x] Create Postgres schema (`tracked_objects`, `orbital_snapshots`, `pipeline_runs`)
- [x] Create S3 bucket with folder structure and lifecycle rules (raw data → Glacier after 90 days)
- [ ] Write a one-off script to backfill a historical snapshot (e.g., last 30 days from space-track.org)
- [ ] Add backfill APIs to run proactively.
- [ ] Set up Snowflake schema mirroring Postgres for historical analytics
- [ ] Define Flask API endpoints and response shapes:
    - `GET /objects?date=&type=&orbit=` — filtered list with lat/lon/alt
    - `GET /objects/:norad_id` — full detail + recent TLE history
    - `GET /snapshot/dates` — available historical dates
- [ ] Connect UI to real API (replace dummy data)

---

### Phase 3: Build Pipeline

**Target:** Fully automated daily ingestion, transformation, and load with monitoring.

Tasks:

- [x] Register space-track.org API credentials; test rate limits (limited to ~200 requests/hr)
- [ ] Write script function: fetch daily delta from space-track.org → upload raw JSON to S3
- [ ] Set up Cron to trigger script daily (e.g., 02:00 UTC)
- [ ] Write Airflow DAG:
    1. Trigger: S3 file sensor detects new raw file
    2. Validate: row count, schema check, null NORAD IDs
    3. Transform: parse TLE → compute lat/lon/alt using `sgp4`; normalize fields
    4. Load: upsert into Postgres `orbital_snapshots`; append to Snowflake
    5. Notify: Slack/email alert on failure
- [ ] Add idempotency: re-running a DAG for the same date should not duplicate records
- [ ] Dashboard: Airflow UI + a simple pipeline health endpoint in Flask

---

### Phase 4: Release

**Target:** Publicly accessible, stable, and monitored application.

Tasks:

- [ ] Containerize Flask API (Docker) and deploy to AWS ECS Fargate or a small EC2 instance
- [ ] Host frontend on AWS S3 + CloudFront (static site)
- [ ] Set up domain and HTTPS (Route 53 + ACM certificate)
- [ ] Add API caching layer (Redis or CloudFront cache) to avoid hammering Postgres on every map load
- [ ] Add basic auth or rate limiting on the Flask API to prevent abuse
- [ ] Set up CloudWatch alarms: Lambda errors, API 5xx rate, Airflow DAG failures
- [ ] Load test the API with a simulated ~10k object payload
- [ ] Write a simple README with architecture diagram

---

### Open Questions / Decisions:

- **TLE propagation:** Compute lat/lon at ingest time (stored) vs. compute on-the-fly in the API (real-time position).
  Stored is simpler; real-time is more accurate for live tracking.
- **Update frequency:** Daily is straightforward. If near-real-time is wanted later, space-track.org supports more
  frequent pulls for active satellites.
- **Snowflake cost:** Only needed if historical analytics queries become heavy. Could start with just Postgres and
  migrate later.
- **3D vs 2D priority:** 3D globe is visually impressive but harder to filter/read dense data. 2D map may be more useful
  for analysis.
