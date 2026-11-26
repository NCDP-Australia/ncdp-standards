# Coastal change indicators (L4) and site reports

The L4 products turn every archived survey of a location into decision-ready indicators: where the
beach is, where its shoreline and backshore sit and move, how much sand it gains or loses, how it
behaves, and whether recent change warrants a warning. They follow the indicator framework of
McCarroll et al. (2024), the beach classification and behavioural analysis of Pucino et al. (2021)
and transect-based beach-profile methods, with **one set of settings for every NCDP location**
so locations can be compared. Results are shown on the Data map at
[ncdp.auscope.org.au/data](https://ncdp.auscope.org.au/data) and in the site reports.

Every run recomputes the whole record of a location from the archived surveys; nothing is updated
incrementally. The full program is rerun every week (Saturday night, Australian Eastern time).

## The common basis

**P1 footprint.** The area each orthomosaic covers.

**P2 beach mask and envelope.** Each survey's orthomosaic is classified into sand and other surfaces
(clustering with per-location, illumination-matched reference masks). The location's **envelope** is
the area that is beach in at least half of the surveys that covered it, so one odd survey or a
partial flight does not move it. The envelope is split by how often it was surveyed: the parts covered
by at least half of all surveys are the **regularly surveyed beach**, the rest (covered by fewer than
half, at least 3) the **occasionally surveyed beach**. Values are computed on the regularly surveyed
beach only; the occasionally surveyed beach is shown for context. (In the data files the field `tier`
keeps the values `core` and `extended` for these two.) Until a person has reviewed a location's mask,
reports say so.

**S4 transects.** The shore-normal transects of Digital Earth Australia Coastlines, 30 m apart, with
two more added between each pair (about 10 m spacing; the actual average is reported, as crossing and
over-long transects are removed). DEA's own transects keep their DEA identifier. They are clipped to the
envelope and run from its landward edge (the baseline) to the sea; a transect belongs to the part of the
envelope that holds most of its length, and its alongshore distance is measured from the first transect. Each survey's DSM is sampled every 0.5 m along
every transect with that date's water masked. A transect counts on a date only when at least 80 % of
its envelope segment is covered by the DSM and at least half of that is not water. A point more than
2.5 m from its own median across dates is excluded on that date.

## The shoreline datum

The shoreline proxy is the **mean high water springs** contour in AHD. On the open coast wave setup
lifts the morphological shoreline above MHWS, which is why the Victorian convention of 1.0 m AHD on the
open coast and 0.5 m AHD in Port Phillip Bay works. To keep locations comparable, the datum is one
fixed value per **class**, decided by two physical parameters recorded for every location:

| Tidal regime (spring range) | Sheltered (enclosed bay, fetch-limited) | Open coast (ocean swell) |
|---|---|---|
| **Microtidal** < 2 m | 0.5 m AHD | 1.0 m AHD |
| **Mesotidal** 2–4 m | MHWS, rounded to 0.5 m | MHWS + 0.5 m setup, rounded to 0.5 m |
| **Macrotidal** > 4 m | MHWS, rounded to 0.5 m | MHWS + 0.5 m setup, rounded to 0.5 m |

The Victorian classes follow DEECA's own designation of every VCMP site (VCMP Sites Data Product,
March 2024: Open Coast or Bay) with the spring tidal range from the VCMP site descriptions: the Port
Phillip Bay and Western Port sites are sheltered (0.5 m AHD), every other Victorian site is open coast
(1.0 m AHD). Cowes and Flinders in Western Port are mesotidal, so there the 0.5 m is recorded as an
override of the rule, with the reason, rather than as its result. Other states default to microtidal and
open until classed. The class, its parameters and where they came from are kept per location
(Admin → Archive → Locations), every indicator file records the datum used, and the site report states
it ("0.5 m AHD (microtidal, sheltered)"). A change of class recomputes the location's whole record;
different datums are never mixed within a location. An override of the rule for one location is
possible but must carry a reason, and the report says the datum was set for that location.

## Position, width and slope

| Indicator | Definition |
|---|---|
| **S1 shoreline** | First crossing of the location's **shoreline datum** walking seaward from the dune-toe baseline (see *The shoreline datum* below). Position in metres from the baseline. Reason codes: crossing, above (dry beach beyond the envelope edge; censored), below (whole transect under the datum), nodata; multiple crossings are counted and flagged. |
| **S2 backshore** | First crossing of **2.5 m AHD**, sampling each transect from 50 m landward of the envelope: about the dune toe or the foot of a structure. |
| **S6 beach width** | Distance from the dune-toe baseline to the shoreline, i.e. the S1 position. |
| **S5 beach slope** | Linear fit to the valid profile. |

## Change

| Indicator | Definition |
|---|---|
| **C1 mean elevation change (MEC)** | Mean height difference over every point inside the envelope covered by both DSMs and not under water on either date. Transect pairs with \|MEC\| > 1.0 m are not a beach process: excluded and counted. Cumulative MEC is the running sum. |
| **C2 unit volume** | Profile area above **0 m AHD** per metre of beach. Change between consecutive surveys is summed over points valid on both dates, so coverage differences do not read as change; the trend is a linear fit of the cumulative change. Site totals multiply by the transect spacing. The trend is a straight least-squares line. |
| **C4 shoreline trend** | Per transect, where it has a crossing on at least 5 dates spanning a year. **Long term:** linear trend over the whole record with the annual cycle removed (sine/cosine term; plain linear below 6 dates). **Short term:** plain linear trend over the last two complete calendar years (McCarroll et al., 2024); it describes those years and is not a projection. |
| **C5 behavioural regime (r-BCD)** | Point elevation changes of every survey pair are put into five equal-frequency classes over the location. Per transect r-BCD = 100 × (share in the two erosional classes − share in the two accretional classes) (Pucino et al., 2021). National class edges −9, −3, 3, 9 give five regimes from strongly accretional to strongly erosional; a transect needs at least a third of the pairs. Net change and behaviour need not agree. |

## The frequently surveyed stretch: record-wide values on fixed ground

Surveys do not always cover the same beach: a location's coverage often grows over the years. Site
values taken over "whatever was surveyed that day" would then jump when new ground joins the record,
and running sums would add up different stretches. Record-wide values and every series over time
(median width, slope and shoreline position, cumulative MEC, unit volume and its trend, the long-term
shoreline trend) therefore use the **frequently surveyed stretch**, part of the regularly surveyed
beach:

- transects of the regularly surveyed beach valid on at least **60 %** of the dates,
- in runs at least **100 m** long (no isolated transects),
- and only the dates on which at least **80 %** of the stretch is valid; pairs compare consecutive such dates.

When too few transects qualify (fewer than 10, or 10 % of the regularly surveyed beach), the whole
regularly surveyed beach is used. The two-year window values, the per-transect values and the erosion
warning use every transect of the regularly surveyed beach.

So the beach is used in three parts, from the most to the least often surveyed:

| Part | How often surveyed | Used for |
|---|---|---|
| **Frequently surveyed stretch** | transects valid on ≥ 60 % of the surveys, in runs ≥ 100 m; uses the surveys covering ≥ 80 % of it | every record-wide series and total |
| **Regularly surveyed beach** | envelope covered by ≥ 50 % of the surveys | values per transect, per-survey medians, the two-year window (short-term trend, erosion warning, hotspots) |
| **Occasionally surveyed beach** | envelope covered by < 50 % of the surveys (at least 3) | shown for context, never in a value |

Reports give each part's share of the surveys, transects, length, alongshore distance, area and surveys
used in one table, a map of the three parts, a chart of the transects with data on each date, and the
data used at each step (surveys, pairs and transects, and why the numbers fall). Figures along the beach
show the regularly surveyed beach as a dashed box with the frequently surveyed stretch shaded inside it
and the occasionally surveyed beach shaded orange; distances are alongshore distances from the first
transect.

## D1 erosion warning indicator

Following McCarroll et al. (2024): six statistics over a two-calendar-year window, each scored 0 (low), 1 (moderate) or 2 (high);
the indicator is the percentage of the points possible. **Low < 25, moderate 25–49, high ≥ 50.**

| Statistic | Value | Moderate / high |
|---|---|---|
| 1 LT long-term shoreline trend | median of Digital Earth Australia Coastlines rates of change rated good along the regularly surveyed beach (Bishop-Taylor et al., 2021), 1988 onwards | ≤ −0.3 / ≤ −0.5 m/yr |
| 2 ST short-term shoreline trend | site mean of the transects' short-term trends | ≤ −2.0 / ≤ −4.0 m/yr |
| 3 SR shoreline eroding | share of transects retreating faster than 4 m/yr | ≥ 20 % / ≥ 40 % |
| 4 BR backshore eroding | share of transects whose backshore retreats faster than 2 m/yr | ≥ 10 % / ≥ 20 % |
| 5 BH strongest backshore erosion | strongest 90 m alongshore mean of the backshore trend (see *Ends, gaps and set-aside stretches*) | ≤ −4.0 / ≤ −8.0 m/yr |
| 6 BW beach width | latest against mean width (mean over transects with a width on most dates) | < 100 % / < 80 % or < 5 m |

The median in statistic 1 keeps a few extreme points (an inlet mouth, a structure) from deciding it.
Indicators flag where change is worth a closer look; they are not forecasts.

## D2 erosion hotspots

Each transect's short-term trend is smoothed over **90 m** alongshore; up to **three** erosion peaks
at least **150 m** apart and at least as strong as the eroding threshold (4 m/yr shoreline, 2 m/yr
backshore) are kept, separately for the shoreline and the backshore.

### Ends, gaps and set-aside stretches

Peaks and statistic 5 count only where the 90 m window is at least **75 %** filled and at least
**90 m** from the ends of the covered beach and from gaps in coverage, so a few transects at the edge
of a survey do not decide them. The line drawn in the report still shows every value.

A location can also have **stretches set aside**, such as river and creek mouths or structures,
where change is real but is not beach erosion in the management sense. They are given by transect
number with a reason (NCDP portal: Admin → Archive → Locations; stored in the pipeline's
`sites/<Location>.json` as `hotspot_exclude`). Set-aside stretches produce no hotspot and do not count
for statistic 5; statistics 2–4 still use every transect. Reports name each stretch and its reason and
show it grey in the trend chart and the hotspot maps. Transect numbers follow a location's transects
and can shift if its envelope changes; each run records the national DEA transect ids at both ends of
every stretch so this can be checked.

## Site reports

A site report (PDF, from the report card) is set out like a paper, with one numbered section per
metric; each section gives **how it is calculated**, then the **results**, with numbers and figures and
no interpretation:

1. Site and survey record (the surveys and their contributors, a map of the envelope and transects)
2. Waves and tides (below)
3. Survey data and analysis domain (the three parts of the beach above)
4. Shoreline position and trends
5. Beach profile, width, slope and backshore (mean profiles of three alongshore sectors)
6. Elevation and volume change
7. Behavioural regime
8. Erosion warning indicator (D1)
9. Erosion hotspots (D2)
10. Processing and parameters (every setting used, the data-quality rules above, references)

Its summary opens with the record-wide change on the frequently surveyed stretch and the current erosion
warning, so the first sentence is not one-sided.

### Waves and tides

Each report describes the beach's wave and tide setting, with a map of the beach, the wave model cell
and the nearest tide gauge on a regional basemap.

- **Waves** come from the CAWCR Wave Hindcast (CSIRO and the Bureau of Meteorology, WAVEWATCH III;
  Durrant et al., 2014, extended monthly): 4 arc-minute grid (about 7 km), hourly from January 1979,
  read every 3 hours. The cell used is the nearest wet cell at least 5 m deep within ±80° of the
  beach's shore normal, so it lies offshore of the beach and not in an estuary behind it. The values are
  offshore model values: no refraction, sheltering or breaking at the beach; in bays they are indicative.
  The report gives the median, 95th and 99th percentile and maximum significant wave height (Hs), the peak
  period, the dominant directions (a wave rose with the beach's seaward direction) and the seasons.
- **Tides** at the beach are modelled with EOT20 (Hart-Davis et al., 2021) through eo-tides
  (Bishop-Taylor et al., 2025), hourly over 2007–2025: mean daily range (MHHW − MLLW), spring range,
  tide type and HAT. The nearest ANCHORS tide gauge of the Bureau of Meteorology (Hague et al., 2022)
  within 150 km shows how well the model does nearby (observed against modelled range; the modelled
  range is called uncertain when they differ by more than 0.2 m) and gives mean sea level in m AHD. An
  open-coast beach is compared only with open-coast gauges, not those in bays, gulfs, harbours or
  behind entrances; if there is none within 150 km the report says so.

Each report comes in two versions, chosen when it is requested:

- **Technical report**: everything above, with the methods, tables and data-quality notes, for councils,
  engineers and consultants. Sections can be chosen; the site and its surveys and the methods are always
  included.
- **Overview**: two to three pages in plain language for community groups and the public, built from the
  same numbers: what is happening at the beach (shoreline movement in metres a year, beach width then and
  now), the erosion warning in the indicator's own words (*low*, *moderate*, *high*, so the two versions are
  never read as different assessments), where it is changing most, what this means and does not, and how
  the surveys are made and by whom.

### Indicator data

Every location's indicators are also published as data, in its location-level `L4` folder
(`<State>/<Location>/L4/` in the archive) and on the site's Analysis page, as one download,
`<Location>_L4_data.zip`:

| File | Contents |
|---|---|
| `<Location>_L4.gpkg` | GeoPackage with every layer: envelope, transects with their metrics, shoreline and backshore points and lines per date, hotspots |
| `shapefiles/` | The same layers as shapefiles (field names cut to 10 characters, so the GeoPackage and CSVs keep the full names) |
| `csv/transects.csv` | One row per transect: alongshore distance (`chainage_m`), part of the beach (`tier`: `core` = regularly, `extended` = occasionally surveyed), long- and short-term shoreline trends, latest position, backshore trend, net elevation and volume change, r-BCD, regime |
| `csv/shoreline_positions.csv`, `csv/backshore_positions.csv` | Transect × survey date: position and reason code |
| `csv/survey_metrics.csv` | One row per survey: median beach width and slope, valid transects, median shoreline position |
| `csv/hotspots.csv` | D2 hotspots, when scored |
| `csv/site_summary.csv` | Record-wide values, the frequently surveyed stretch (extent, transects, surveys and its record-wide values), the shoreline datum and its class, and the erosion warning with its status and statistics |
| `reports/` | The technical report and the overview (PDF) |
| `README.txt` | What each file and column is, units, datum, method, citation; and what is not included, and why |

All in GDA2020 / MGA (the location's zone), heights in metres AHD.

Every report credits the surveys to the organisations that flew and processed them and to the
programs that funded them, read from each survey's metadata (`Organisation`, `Record Funded
Programmes`): for example "contributed by Deakin University under the Victorian Coastal Monitoring
Program (VCMP), funded by the Department of Energy, Environment and Climate Action". The National
Coastal Drone Program coordinates, archives and analyses the surveys; it does not fly them, and a
report never says it did. A survey with no organisation in its metadata is counted as "without
contributor metadata" rather than credited to anyone.

## References

- Bishop-Taylor, R., Phillips, C., Sagar, S., Newey, V., & Sutterley, T. (2025). eo-tides: Tide modelling tools for large-scale satellite Earth observation analysis. *Journal of Open Source Software*.
- Bishop-Taylor, R., Nanson, R., Sagar, S., & Lymburner, L. (2021). Mapping Australia's dynamic coastline at mean sea level using three decades of Landsat imagery. *Remote Sensing of Environment*, 267, 112734. https://doi.org/10.1016/j.rse.2021.112734
- Durrant, T., Greenslade, D., Hemer, M., & Trenham, C. (2014). *A global wave hindcast focussed on the Central and South Pacific*. CAWCR Technical Report No. 070. Centre for Australian Weather and Climate Research. Data: CAWCR Wave Hindcast, CSIRO, https://doi.org/10.4225/08/523168703DCC5
- Hague, B. S., Jones, D. A., Trewin, B., Jakob, D., Murphy, B. F., Martin, D. J., & Braganza, K. (2022). ANCHORS: A multi-decadal tide gauge dataset to monitor Australian relative sea level changes. *Geoscience Data Journal*, 9(2). https://doi.org/10.1002/gdj3.136. Data: https://doi.org/10.25914/6142dff37250b
- Hart-Davis, M. G., Piccioni, G., Dettmering, D., Schwatke, C., Passaro, M., & Seitz, F. (2021). EOT20: a global ocean tide model from multi-mission satellite altimetry. *Earth System Science Data*, 13, 3869–3884. https://doi.org/10.5194/essd-13-3869-2021
- McCarroll, R. J., Kennedy, D. M., Liu, J., Allan, B., & Ierodiaconou, D. (2024). Design and application of coastal erosion indicators using satellite and drone data for a regional monitoring program. *Ocean & Coastal Management*, 253, 107146. https://doi.org/10.1016/j.ocecoaman.2024.107146
- Pucino, N., Kennedy, D. M., Carvalho, R. C., Allan, B., & Ierodiaconou, D. (2021). Citizen science for monitoring seasonal-scale beach erosion and behaviour with aerial drones. *Scientific Reports*, 11, 3935. https://doi.org/10.1038/s41598-021-83477-6
