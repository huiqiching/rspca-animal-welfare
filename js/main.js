// =====================================================================
// main.js: embeds every Vega-Lite chart on the page.
// Each chart's specification lives in its own .vg.json file in /js
// so the JSON is easy to find and read in the GitHub repository.
// =====================================================================

// Shared theme: fonts and colours that match css/style.css.
// Passed to vegaEmbed as "config", so every chart looks consistent
// without repeating the same settings in every spec.
//
// Colour rule: species colours are reserved for animal categories.
// Everything else (quantities, totals, text, axes, maps) uses one
// desaturated slate system, so it never competes with the species colours.
const PALETTE = {
  species: {
    dogs: "#F5A01A",      // amber
    cats: "#0085CA",      // RSPCA blue
    wildlife: "#3B7F2A",  // green
    other: "#A1887F"      // taupe
  },
  waMoreReports: "#7B1FA2", // purple, WA map only
  sequential: ["#E6EAEF", "#BDC3CC", "#939AA6", "#646B76", "#2D333D"], // light to dark
  neutralMark: "#2D333D",   // aggregate lines, points, nodes
  neutralSoft: "#D3D8DF",   // background shapes, lollipop stems
  canvas: "#FFFFFF",        // chart background (cards)
  page: "#F9FAFC",          // page background
  mapBorder: "#FFFFFF",     // stroke between filled regions
  basemap: "#ECEEF2",       // context land under symbols
  noDataFill: "#FFFFFF",    // no data: white fill...
  noDataStroke: "#8E95A0",  // ...with a dashed [3,2] outline
  ink: "#2D333D",
  inkSoft: "#5D646E",
  grid: "#E7EAEE",
  axis: "#B5BBC4"
};

const theme = {
  background: "transparent",
  font: "Source Sans 3",
  view: { stroke: null },
  axis: {
    labelFont: "Source Sans 3",
    titleFont: "Source Sans 3",
    labelFontSize: 13,
    titleFontSize: 13,
    titleFontWeight: 600,
    labelColor: PALETTE.inkSoft,
    titleColor: PALETTE.inkSoft,
    gridColor: PALETTE.grid,
    domainColor: PALETTE.axis,
    tickColor: PALETTE.axis
  },
  legend: {
    labelFont: "Source Sans 3",
    titleFont: "Source Sans 3",
    labelFontSize: 13,
    titleFontSize: 13,
    titleFontWeight: 600,
    labelColor: PALETTE.ink,
    titleColor: PALETTE.inkSoft
  },
  header: {
    labelFont: "Fraunces",
    labelFontSize: 15,
    labelFontWeight: 600,
    labelColor: PALETTE.ink,
    titleFont: "Source Sans 3"
  },
  range: { ramp: PALETTE.sequential },
  text: { font: "Source Sans 3", fontSize: 12, color: PALETTE.ink }
};

const embedOptions = {
  actions: false,     // hides the "..." menu / "Open in Vega Editor" button
  renderer: "svg",    // crisp text and shapes at any zoom level
  config: theme
};

// [div id on the page, path to the Vega-Lite specification]
const charts = [
  ["#waffle_species",   "js/1_waffle_species.vg.json"],
  ["#trend_received",   "js/2a_trend_received.vg.json"],
  ["#slope_euthanasia", "js/2b_slope_euthanasia.vg.json"],
  ["#map_complaints",   "js/3a_choropleth_complaints.vg.json"],
  ["#map_received",     "js/3b_symbol_map_received.vg.json"],
  ["#change_received",  "js/3c_change_received.vg.json"],
  ["#dorling_live",     "js/4a_dorling_live_release.vg.json"],
  ["#heatmap_reasons",  "js/4b_heatmap_euthanasia_reasons.vg.json"],
  ["#squares_court",    "js/5a_squares_complaint_to_court.vg.json"],
  ["#trend_court",      "js/5b_trend_prosecutions.vg.json"],
  ["#map_wa",           "js/5c_wa_hotspots_map.vg.json"],
  ["#sankey_outcomes",  "js/6a_sankey_outcomes.vg.json"],
  ["#dotplot_wa",       "js/6b_dotplot_wa_adoption.vg.json"]
];

charts.forEach(function ([divId, specPath]) {
  vegaEmbed(divId, specPath, embedOptions).catch(console.error);
});
