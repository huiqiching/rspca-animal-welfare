// =====================================================================
// main.js: embeds every Vega-Lite chart on the page.
// Each chart's specification lives in its own .vg.json file in /js
// so the JSON is easy to find and read in the GitHub repository.
// =====================================================================

// Shared theme: fonts and colours that match css/style.css.
// Passed to vegaEmbed as "config", so every chart looks consistent
// without repeating the same settings in every spec.
//
// Colours come from the RSPCA Australia website (navy #002133, RSPCA blue #0085CA,
// light blue #9FD0EA, green, amber), adjusted and checked so every pair stays
// distinguishable for people with colour-vision deficiency.
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
    labelColor: "#4A5A66",
    titleColor: "#4A5A66",
    gridColor: "#E6EBEE",
    domainColor: "#B8C2C8",
    tickColor: "#B8C2C8"
  },
  legend: {
    labelFont: "Source Sans 3",
    titleFont: "Source Sans 3",
    labelFontSize: 13,
    titleFontSize: 13,
    titleFontWeight: 600,
    labelColor: "#002133",
    titleColor: "#4A5A66"
  },
  header: {
    labelFont: "Fraunces",
    labelFontSize: 15,
    labelFontWeight: 600,
    labelColor: "#002133",
    titleFont: "Source Sans 3"
  },
  text: { font: "Source Sans 3", fontSize: 12, color: "#002133" }
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
  ["#dorling_live",     "js/4a_dorling_live_release.vg.json"],
  ["#heatmap_reasons",  "js/4b_heatmap_euthanasia_reasons.vg.json"],
  ["#squares_court",    "js/5a_squares_complaint_to_court.vg.json"],
  ["#trend_court",      "js/5b_trend_prosecutions.vg.json"],
  ["#map_wa",           "js/5c_wa_hotspots_map.vg.json"]
];

charts.forEach(function ([divId, specPath]) {
  vegaEmbed(divId, specPath, embedOptions).catch(console.error);
});
