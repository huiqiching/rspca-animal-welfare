"""Build Vega-Lite-ready (tidy/long) CSVs for FIT3179 DV2 - RSPCA Animal Welfare.
All numbers transcribed from:
  [A] RSPCA Australia National Statistics 2024-2025 (PDF)
  [B] ABS media release 'Population up 1.5% in June 2025' (18 Dec 2025)
  [C] RSPCA WA 'RSPCA WA reveals state's animal cruelty hotspots' (2023-24 data)
  [D] RSPCA WA 2024-25 Impact Statement (PDF)
"""
import csv, os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

STATES = ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"]
STATE_NAME = {"ACT": "Australian Capital Territory", "NSW": "New South Wales",
              "NT": "Northern Territory", "QLD": "Queensland", "SA": "South Australia",
              "TAS": "Tasmania", "VIC": "Victoria", "WA": "Western Australia"}

def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")

# ---------------------------------------------------------------- [A] Table 4
# species -> outcome -> values in STATES order
T4 = {
 "Dogs": {
  "Reclaimed": [109,0,229,1647,501,0,646,71], "Returned": [75,18,243,204,33,48,83,23],
  "Rehomed": [310,119,1350,2922,867,220,704,347], "Currently in care": [60,53,442,397,204,91,199,226],
  "Transferred": [5,0,162,63,49,0,159,91], "Euthanased": [36,14,878,1133,303,20,210,174],
  "Other": [0,0,16,35,6,0,14,43]},
 "Cats": {
  "Reclaimed": [120,1,122,443,117,0,157,19], "Returned": [33,0,116,99,51,22,39,21],
  "Rehomed": [1433,186,3863,4992,2191,488,2688,604], "Currently in care": [171,58,607,543,251,73,344,81],
  "Transferred": [2,2,40,87,58,0,81,28], "Euthanased": [151,9,1768,1772,663,109,471,146],
  "Other": [25,3,105,83,24,8,50,21]},
 "Horses": {
  "Reclaimed": [0,0,0,2,0,0,0,0], "Returned": [0,0,1,2,0,0,2,0],
  "Rehomed": [0,0,31,8,0,2,131,6], "Currently in care": [0,0,44,9,39,3,69,17],
  "Transferred": [0,0,1,1,18,0,34,1], "Euthanased": [0,0,24,5,9,5,67,2],
  "Other": [0,0,2,0,0,0,2,0]},
 "Livestock": {
  "Reclaimed": [0,0,1,13,13,0,0,3], "Returned": [0,0,41,2,1,0,1,0],
  "Rehomed": [43,2,104,234,40,28,32,68], "Currently in care": [7,0,15,32,98,26,19,5],
  "Transferred": [0,0,46,16,94,0,21,8], "Euthanased": [11,0,50,196,26,2,20,25],
  "Other": [0,0,2,16,7,0,3,4]},
 "Wildlife": {
  "Released": [1,0,1,2521,59,0,13,0], "Currently in care": [4,0,3,172,13,0,8,0],
  "Transferred": [27,0,103,5591,173,0,18,0], "Euthanased": [71,0,301,17307,103,0,239,0],
  "Other": [5,0,11,973,13,0,64,0]},
 "Other animals": {
  "Reclaimed": [19,24,0,2,10,8,12,4], "Returned": [8,0,215,23,12,0,7,3],
  "Rehomed": [191,0,646,652,241,71,651,269], "Currently in care": [8,0,117,222,226,8,743,32],
  "Transferred": [1,0,167,34,118,0,55,6], "Euthanased": [17,0,476,421,128,1,105,32],
  "Other": [11,0,54,94,26,0,40,11]},
}
TOTALS_2425 = {"Dogs": [595,204,3320,6401,1963,379,2015,975],
               "Cats": [1935,259,6621,8019,3355,700,3830,920],
               "Horses": [0,0,103,27,66,10,305,26],
               "Livestock": [61,2,259,509,279,56,96,113],
               "Wildlife": [108,0,419,26564,361,0,342,0],
               "Other animals": [249,0,1688,1521,772,80,1601,356]}
TOTALS_2324 = {"Dogs": [676,310,4554,6531,1814,130,2550,903],
               "Cats": [2065,357,7007,7650,3033,1063,4611,918],
               "Horses": [0,0,142,51,24,19,231,16],
               "Livestock": [88,0,406,404,310,2,176,98],
               "Wildlife": [205,0,468,27423,328,10,650,0],
               "Other animals": [333,17,1898,1931,489,121,1155,502]}
STATE_TOTAL_2425 = [2948,465,12410,43041,6796,1225,8189,2390]
STATE_TOTAL_2324 = [3367,684,14475,43990,5998,1345,9373,2437]

# outcome grouping, useful for colour encoding / stacking order
OUTCOME_GROUP = {"Reclaimed": "Live outcome", "Returned": "Live outcome", "Rehomed": "Live outcome",
                 "Released": "Live outcome", "Currently in care": "Still in care",
                 "Transferred": "Transferred", "Euthanased": "Euthanased", "Other": "Other (incl. died in care)"}
OUTCOME_ORDER = {"Rehomed": 1, "Reclaimed": 2, "Returned": 3, "Released": 4, "Currently in care": 5,
                 "Transferred": 6, "Other": 7, "Euthanased": 8}

# --- validation: outcomes sum to the published species totals per state
errors = 0
for sp, outs in T4.items():
    for i, st in enumerate(STATES):
        s = sum(v[i] for v in outs.values())
        if s != TOTALS_2425[sp][i]:
            print(f"MISMATCH {sp} {st}: outcomes={s} published={TOTALS_2425[sp][i]}"); errors += 1
for i, st in enumerate(STATES):
    for label, tot, pub in [("24-25", TOTALS_2425, STATE_TOTAL_2425), ("23-24", TOTALS_2324, STATE_TOTAL_2324)]:
        s = sum(tot[sp][i] for sp in tot)
        if s != pub[i]:
            print(f"MISMATCH state total {label} {st}: {s} vs {pub[i]}"); errors += 1
assert sum(STATE_TOTAL_2425) == 77464 and sum(STATE_TOTAL_2324) == 81669
print("validation errors:", errors)

rows = []
for sp, outs in T4.items():
    for out, vals in outs.items():
        for i, st in enumerate(STATES):
            rows.append(["2024-25", 2025, st, STATE_NAME[st], sp, out, OUTCOME_GROUP[out],
                         OUTCOME_ORDER[out], vals[i]])
write("rspca_state_species_outcomes_2024_25.csv",
      ["fin_year", "year_end", "state", "state_name", "species", "outcome", "outcome_group",
       "outcome_order", "count"], rows)

rows = []
for label, ye, tot in [("2023-24", 2024, TOTALS_2324), ("2024-25", 2025, TOTALS_2425)]:
    for sp, vals in tot.items():
        for i, st in enumerate(STATES):
            rows.append([label, ye, st, STATE_NAME[st], sp, vals[i]])
write("rspca_state_species_received_2023_2025.csv",
      ["fin_year", "year_end", "state", "state_name", "species", "received"], rows)

# ---------------------------------------------------------------- [A] Table 2
YEARS5 = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
T2 = {"Dogs": {"Live/other outcome": [19809,16737,15903,14626,13084], "Euthanased": [2502,2484,2875,2842,2768]},
      "Cats": {"Live/other outcome": [33968,29065,27523,21556,20550], "Euthanased": [8604,6506,6224,5148,5089]},
      "Other animals (incl. wildlife, horses, livestock)": {
          "Live/other outcome": [17597,18983,18228,16480,16330], "Euthanased": [20577,21053,16712,21017,19643]}}
T2_TOT = {"Dogs": [22311,19221,18778,17468,15852], "Cats": [42572,35571,33747,26704,25639],
          "Other animals (incl. wildlife, horses, livestock)": [38174,40036,34940,37497,35973]}
NAT_TOT = [103057,94828,87465,81669,77464]
rows = []
for sp, d in T2.items():
    for j, y in enumerate(YEARS5):
        a, e = d["Live/other outcome"][j], d["Euthanased"][j]
        assert a + e == T2_TOT[sp][j], (sp, y)
        tot = T2_TOT[sp][j]
        rows.append([y, int(y[:4]) + 1, sp, a, e, tot, round(100 * e / tot, 2)])
for j in range(5):
    assert sum(T2_TOT[s][j] for s in T2_TOT) == NAT_TOT[j]
write("rspca_national_trend_5yr.csv",
      ["fin_year", "year_end", "species_group", "reclaimed_returned_rehomed_other", "euthanased",
       "total_received", "pct_euthanased"], rows)

# long version for stacked / streamgraph use
rows = []
for sp, d in T2.items():
    for outc, vals in d.items():
        for j, y in enumerate(YEARS5):
            rows.append([y, int(y[:4]) + 1, sp, outc, vals[j]])
write("rspca_national_trend_5yr_long.csv",
      ["fin_year", "year_end", "species_group", "outcome", "count"], rows)

# ---------------------------------------------------------------- [A] Table 3
T3 = {"Dogs": {"Infectious": [0,0,6,28,3,0,4,22], "Medical": [25,7,235,410,109,17,97,40],
               "Behavioural": [11,7,627,672,161,3,100,71], "Legal": [0,0,2,19,20,0,6,7],
               "Other": [0,0,8,4,10,0,3,34]},
      "Cats": {"Infectious": [2,0,246,348,31,0,39,0], "Medical": [69,6,871,932,237,24,157,83],
               "Behavioural": [80,3,321,473,383,85,179,52], "Legal": [0,0,0,2,0,0,47,0],
               "Other": [0,0,330,17,12,0,49,11]}}
rows = []
for sp, d in T3.items():
    for i, st in enumerate(STATES):
        assert sum(v[i] for v in d.values()) == T4[sp]["Euthanased"][i], (sp, st)
    for reason, vals in d.items():
        for i, st in enumerate(STATES):
            rows.append(["2024-25", st, STATE_NAME[st], sp, reason, vals[i]])
write("rspca_euthanasia_reasons_2024_25.csv",
      ["fin_year", "state", "state_name", "species", "reason", "count"], rows)

# ---------------------------------------------------------------- [A] Table 5 (no NT: RSPCA NT cannot enforce)
INSP_STATES = ["ACT", "NSW", "QLD", "SA", "TAS", "VIC", "WA"]
T5 = {"complaints_investigated": [744,16713,13874,5125,1915,10206,7195],
      "prosecutions_finalised": [5,226,3,37,2,47,61],
      "successful_prosecutions": [5,119,0,32,2,47,59],
      "charges_laid": [0,991,0,192,56,204,165],
      "people_charged": [5,0,3,44,4,49,59],
      "cases_pending": [0,104,0,46,20,19,46],
      "routine_inspections": [9,49,0,8,31,12,0]}
assert sum(T5["complaints_investigated"]) == 55772 and sum(T5["prosecutions_finalised"]) == 381
rows = [["2024-25", st, STATE_NAME[st]] + [T5[k][i] for k in T5] for i, st in enumerate(INSP_STATES)]
write("rspca_inspectorate_by_state_2024_25.csv", ["fin_year", "state", "state_name"] + list(T5), rows)
rows = [["2024-25", st, STATE_NAME[st], k, T5[k][i]] for k in T5 for i, st in enumerate(INSP_STATES)]
write("rspca_inspectorate_by_state_2024_25_long.csv",
      ["fin_year", "state", "state_name", "measure", "value"], rows)

# ---------------------------------------------------------------- [A] Table 6
T6 = [("2019-20", 73997, 359), ("2020-21", 73301, 426), ("2021-22", 69014, 318),
      ("2022-23", 69623, 251), ("2023-24", 71514, 248), ("2024-25", 67237, 381)]
rows = [[y, int(y[:4]) + 1, c, p, round(1000 * p / c, 2)] for y, c, p in T6]
write("rspca_national_complaints_prosecutions_6yr.csv",
      ["fin_year", "year_end", "complaints_incl_revisits", "prosecutions_finalised",
       "prosecutions_per_1000_complaints"], rows)

# ---------------------------------------------------------------- [B] ABS population
POP25 = {"NSW": 8593.9, "VIC": 7074.5, "QLD": 5669.8, "SA": 1902.3, "WA": 3043.7,
         "TAS": 576.0, "NT": 264.4, "ACT": 484.8}
CHG = {"NSW": 101.8, "VIC": 123.5, "QLD": 97.9, "SA": 20.2, "WA": 65.6, "TAS": 1.2, "NT": 3.5, "ACT": 6.4}
# approximate geographic centroids (for proportional-symbol placement) - verify against your TopoJSON
CENTROID = {"ACT": (-35.47, 149.01), "NSW": (-32.17, 147.02), "NT": (-19.49, 132.55),
            "QLD": (-22.58, 144.08), "SA": (-30.06, 135.78), "TAS": (-42.02, 146.59),
            "VIC": (-36.85, 144.28), "WA": (-25.33, 122.30)}
rows = []
for st in STATES:
    p25 = round(POP25[st] * 1000); p24 = round((POP25[st] - CHG[st]) * 1000)
    lat, lon = CENTROID[st]
    rows.append([st, STATE_NAME[st], p24, p25, lat, lon])
write("abs_state_population_2024_2025.csv",
      ["state", "state_name", "pop_jun2024", "pop_jun2025", "centroid_lat", "centroid_lon"], rows)

# ---------------------------------------------------------------- derived: per-capita + rates (2024-25)
rows = []
for i, st in enumerate(STATES):
    pop = round(POP25[st] * 1000)
    rec = STATE_TOTAL_2425[i]
    dc_rec = TOTALS_2425["Dogs"][i] + TOTALS_2425["Cats"][i]
    # live release rate (dogs+cats) = (reclaimed+returned+rehomed) / (total - still in care)
    live = sum(T4[s][o][i] for s in ("Dogs", "Cats") for o in ("Reclaimed", "Returned", "Rehomed"))
    incare = sum(T4[s]["Currently in care"][i] for s in ("Dogs", "Cats"))
    euth = sum(T4[s]["Euthanased"][i] for s in ("Dogs", "Cats"))
    exits = dc_rec - incare
    if st in INSP_STATES:
        j = INSP_STATES.index(st)
        comp = T5["complaints_investigated"][j]; pros = T5["prosecutions_finalised"][j]
        comp10k = round(10000 * comp / pop, 2)
        pros_per_1000 = round(1000 * pros / comp, 2)
    else:
        comp = pros = comp10k = pros_per_1000 = ""
    rows.append(["2024-25", st, STATE_NAME[st], pop, rec, round(10000 * rec / pop, 2),
                 dc_rec, round(10000 * dc_rec / pop, 2),
                 TOTALS_2425["Wildlife"][i], round(100 * live / exits, 1) if exits else "",
                 round(100 * euth / exits, 1) if exits else "",
                 comp, comp10k, pros, pros_per_1000,
                 round(100 * (rec - STATE_TOTAL_2324[i]) / STATE_TOTAL_2324[i], 2)])
write("derived_state_rates_2024_25.csv",
      ["fin_year", "state", "state_name", "population", "animals_received", "received_per_10k",
       "dogs_cats_received", "dogs_cats_per_10k", "wildlife_received",
       "dogs_cats_live_release_pct", "dogs_cats_euthanased_pct",
       "complaints_investigated", "complaints_per_10k", "prosecutions_finalised",
       "prosecutions_per_1000_complaints", "pct_change_received_vs_2023_24"], rows)

# ---------------------------------------------------------------- [C] WA LGA hotspots 2023-24
# lat/lon = approximate town/council centre, added for proportional-symbol map; verify before use
WA_LGA = [
 ("Metropolitan", 1, 686, "Swan", 8, 1, -31.89, 116.01),
 ("Metropolitan", 2, 595, "Wanneroo", 13, 2, -31.75, 115.80),
 ("Metropolitan", 3, 399, "Stirling", -9, 3, -31.88, 115.83),
 ("Metropolitan", 4, 395, "Gosnells", 15, 5, -32.08, 116.00),
 ("Metropolitan", 5, 356, "Armadale", -7, 6, -32.15, 116.01),
 ("Metropolitan", 6, 346, "Rockingham", -8, 5, -32.28, 115.73),
 ("Metropolitan", 7, 291, "Mandurah", 8, 7, -32.53, 115.72),
 ("Metropolitan", 8, 272, "Cockburn", 25, 8, -32.12, 115.82),
 ("Metropolitan", 9, 209, "Joondalup", 2, 9, -31.74, 115.77),
 ("Metropolitan", 10, 163, "Belmont", 11, 12, -31.96, 115.93),
 ("Regional", 1, 214, "Greater Geraldton", 14, 2, -28.78, 114.61),
 ("Regional", 2, 158, "Albany", -16, 1, -35.02, 117.88),
 ("Regional", 2, 158, "Bunbury", 8, 4, -33.33, 115.64),
 ("Regional", 3, 116, "Kalgoorlie-Boulder", -27, 3, -30.75, 121.47),
 ("Regional", 4, 112, "Busselton", -7, 5, -33.65, 115.35),
 ("Regional", 5, 74, "Capel", 51, 11, -33.56, 115.56),
 ("Regional", 5, 74, "Harvey", -20, 6, -33.08, 115.89),
 ("Regional", 6, 61, "Broome", -17, 7, -17.96, 122.24),
 ("Regional", 7, 60, "Northam", 20, 10, -31.65, 116.67),
 ("Regional", 8, 49, "Collie", -9, 9, -33.36, 116.16),
 ("Regional", 9, 48, "Plantagenet", 14, 12, -34.63, 117.67),
 ("Regional", 10, 41, "Esperance", -16, 11, -33.86, 121.89),
]
rows = [["2023-24", r, rank, lga, rep, pct, prev, lat, lon]
        for (r, rank, rep, lga, pct, prev, lat, lon) in WA_LGA]
write("rspcawa_cruelty_reports_top_lga_2023_24.csv",
      ["fin_year", "area_type", "rank", "lga", "reports", "pct_change_vs_2022_23",
       "rank_2022_23", "approx_lat", "approx_lon"], rows)

WA_OFF = [("Ill-treatment", 3397, 3296), ("Failure to alleviate harm", 1919, 1604),
          ("Insufficient food/water", 1885, 1507), ("Abandonment", 1165, 1173),
          ("Insufficient shelter", 934, 764), ("Unnecessary harm", 683, 603),
          ("Malicious beating/wounding", 411, 311), ("Harmful containment (vehicle)", 405, 506),
          ("Harmful containment", 263, 203), ("Injured", 108, 147)]
rows = []
for o, a, b in WA_OFF:
    rows += [["2022-23", 2023, o, b], ["2023-24", 2024, o, a]]
write("rspcawa_offences_reported_2022_2024.csv", ["fin_year", "year_end", "offence", "reports"], rows)

# ---------------------------------------------------------------- [D] RSPCA WA 2024-25 impact statement
rows = [["2024-25", k, v] for k, v in [
    ("Calls to cruelty hotline", 26574), ("Calls answered", 16153), ("Cases investigated", 7195),
    ("Animals surrendered", 1193), ("Animals seized", 298), ("Cases prosecuted", 41),
    ("Offenders", 57), ("Pet ownership bans", 49), ("Prison sentences", 7),
    ("Inspectors employed", 16), ("Km travelled by inspectors", 298005)]]
write("rspcawa_inspectorate_funnel_2024_25.csv", ["fin_year", "measure", "value"], rows)

CARE = [("Dogs/puppies", 948, 347), ("Cats/kittens", 911, 604), ("Birds", 56, 20),
        ("Rabbits", 160, 135), ("Horses", 26, 6), ("Livestock", 113, 68),
        ("Guinea pigs", 115, 92), ("Rodents", 28, 22)]
assert sum(c for _, c, _ in CARE) == 2357 and sum(a for *_, a in CARE) == 1294
write("rspcawa_care_and_adoptions_by_type_2024_25.csv",
      ["fin_year", "animal_type", "cared_for", "adopted"], [["2024-25", t, c, a] for t, c, a in CARE])

PROS = [("Dogs", 187), ("Cats/kittens", 9), ("Birds", 14), ("Goats", 19), ("Horses/pony", 6),
        ("Rooster/hens", 3), ("Guinea pig", 1), ("Rats", 2), ("Sheep", 1)]
assert sum(n for _, n in PROS) == 242
write("rspcawa_animals_in_prosecutions_2024_25.csv", ["fin_year", "animal_type", "animals"],
      [["2024-25", t, n] for t, n in PROS])
