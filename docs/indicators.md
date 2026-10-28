# Coastal change indicators (L4) and site reports

The L4 products turn every archived survey of a location into decision-ready indicators: where the
beach is, where its shoreline and backshore sit and move, how much sand it gains or loses, how it
behaves, and whether recent change warrants a warning. They follow the indicator framework of
McCarroll et al. (2024), the beach classification and behavioural analysis of Pucino et al. (2021)
and the transect methods of Nuyts et al. (2026), with **one set of settings for every NCDP location**
so locations can be compared. Results are shown on the Data map at
[ncdp.auscope.org.au/data](https://ncdp.auscope.org.au/data) and in the site reports.

Every run recomputes the whole record of a location from the archived surveys; nothing is updated
incrementally. The full program is rerun on the first day of each month.

## The common basis

**P1 footprint.** The area each orthomosaic covers.

**P2 beach mask and envelope.** Each survey's orthomosaic is classified into sand and other surfaces
(clustering with per-location, illumination-matched reference masks). The location's **envelope** is
the area that is beach in at least half of the surveys that covered it, so one odd survey or a
partial flight does not move it. Parts seen by at least half of all surveys are the **core** tier;
the rest is **extended**. Site values use the core tier only and never mix the tiers. Until a person
has reviewed a location's mask, reports say so.

**S4 transects.** Shore-normal lines anchored to Digital Earth Australia Coastlines (10 m nominal
spacing; the actual average is reported, as crossing and over-long transects are removed), clipped to
the envelope and oriented from the dune toe to the sea. Each survey's DSM is sampled every 0.5 m along
every transect with that date's water masked. A transect counts on a date only when at least 80 % of
its envelope segment is covered by the DSM and at least half of that is not water. A point more than
2.5 m from its own median across dates is excluded on that date.

## Position, width and slope

| Indicator | Definition |
|---|---|
| **S1 shoreline** | First crossing of **1.0 m AHD** walking seaward from the dune-toe baseline. Position in metres from the baseline. Reason codes: crossing, above (dry beach beyond the envelope edge; censored), below (whole transect under the datum), nodata; multiple crossings are counted and flagged. |
| **S2 backshore** | First crossing of **2.5 m AHD**, sampling each transect from 50 m landward of the envelope: about the dune toe or the foot of a structure. |
| **S6 beach width** | Distance from the dune-toe baseline to the shoreline, i.e. the S1 position. |
| **S5 beach slope** | Linear fit to the valid profile. |

## Change

| Indicator | Definition |
|---|---|
| **C1 mean elevation change (MEC)** | Mean height difference over every point inside the envelope covered by both DSMs and not under water on either date. Transect pairs with \|MEC\| > 1.0 m are not a beach process: excluded and counted. Cumulative MEC is the running sum. |
| **C2 unit volume** | Profile area above **0 m AHD** per metre of beach. Change between consecutive surveys is summed over points valid on both dates, so coverage differences do not read as change; the trend is a linear fit of the cumulative change. Site totals multiply by the transect spacing. |
| **C4 shoreline trend** | Per transect, where it has a crossing on at least 5 dates spanning a year. **Long term:** linear trend over the whole record with the annual cycle removed (sine/cosine term; plain linear below 6 dates). **Short term:** plain linear trend over the last two complete calendar years (McCarroll et al., 2024); it describes those years and is not a projection. |
| **C5 behavioural regime (r-BCD)** | Point elevation changes of every survey pair are put into five equal-frequency classes over the location. Per transect r-BCD = 100 × (share in the two erosional classes − share in the two accretional classes) (Pucino et al., 2021). National class edges −9, −3, 3, 9 give five regimes from strongly accretional to strongly erosional; a transect needs at least a third of the pairs. Net change and behaviour need not agree. |

## The reference stretch: record-wide values on fixed ground

Surveys do not always cover the same beach: a location's coverage often grows over the years. Site
values taken over "whatever was surveyed that day" would then jump when new ground joins the record,
and running sums would add up different stretches. Record-wide values and every series over time
(median width, slope and shoreline position, cumulative MEC, unit volume and its trend, the long-term
shoreline trend) therefore use a **reference stretch**:

- core transects valid on at least **60 %** of the dates,
- in runs at least **100 m** long (no isolated transects),
- and only the dates on which at least **80 %** of the stretch is valid; pairs compare consecutive such dates.

When too few transects qualify (fewer than 10, or 10 % of the core), the whole core beach is used.
The two-year window values, the per-transect maps and the erosion warning use every core transect.
Reports state the stretch (length, chainage, number of transects and of surveys) and show a coverage
chart: core transects with data on each date, and how many of them lie on the stretch.

## D1 erosion warning indicator

Six statistics over a two-calendar-year window, each scored 0 (low), 1 (moderate) or 2 (high);
the indicator is the percentage of the points possible. **Low < 25, moderate 25–49, high ≥ 50.**

| Statistic | Value | Moderate / high |
|---|---|---|
| 1 LT long-term shoreline trend | median of Digital Earth Australia Coastlines rates of change rated good along the core beach (Bishop-Taylor et al., 2021), 1988 onwards | ≤ −0.3 / ≤ −0.5 m/yr |
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

A site report (PDF, from the report card) presents: the site and its surveys with the coverage chart;
the beach surface (mean profiles of three alongshore sectors, each with the years of its first
survey); width and slope; shoreline position and trends; elevation and volume change; behavioural
regime; the erosion warning and hotspots; and the methods and data-quality rules above. Its summary
opens with the record-wide change on the reference stretch and the current erosion warning, so the
first sentence is not one-sided.

## References

- Bishop-Taylor, R., Nanson, R., Sagar, S., & Lymburner, L. (2021). Mapping Australia's dynamic coastline at mean sea level using three decades of Landsat imagery. *Remote Sensing of Environment*, 267, 112734. https://doi.org/10.1016/j.rse.2021.112734
- McCarroll, R. J., Kennedy, D. M., Liu, J., Allan, B., & Ierodiaconou, D. (2024). Design and application of coastal erosion indicators using satellite and drone data for a regional monitoring program. *Ocean & Coastal Management*, 253, 107146. https://doi.org/10.1016/j.ocecoaman.2024.107146
- Nuyts, S., Allan, B., Kennedy, D. M., & Ierodiaconou, D. (2026). Beach morphodynamics and coastal armouring at Port Fairy, Victoria (companion papers, in review).
- Pucino, N., Kennedy, D. M., Carvalho, R. C., Allan, B., & Ierodiaconou, D. (2021). Citizen science for monitoring seasonal-scale beach erosion and behaviour with aerial drones. *Scientific Reports*, 11, 3935. https://doi.org/10.1038/s41598-021-83477-6
