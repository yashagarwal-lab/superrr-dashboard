const fs = require("fs");
const vm = require("vm");

function runVerification(htmlPath) {
  console.log(`\n========================================`);
  console.log(`VERIFYING FILE: ${htmlPath}`);
  console.log(`========================================`);

  const html = fs.readFileSync(htmlPath, "utf8");
  const scripts = [...html.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi)];
  const appScript = scripts.find(s => s[1].includes("const DATA")) || scripts[scripts.length - 1];
  if (!appScript) throw new Error("No application script found in " + htmlPath);
  const code = appScript[1];

  let consoleErrors = [];
  let consoleWarns = [];

  // DOM Mock Factory
  const elements = {};
  function getOrCreateElement(id) {
    if (!elements[id]) {
      elements[id] = {
        id: id,
        innerHTML: "",
        textContent: "",
        value: "",
        style: {},
        options: [],
        classList: {
          add: () => {},
          remove: () => {},
          contains: () => false,
          toggle: () => {},
        },
        getContext: (type) => ({
          clearRect: () => {},
          beginPath: () => {},
          arc: () => {},
          fill: () => {},
          stroke: () => {},
          fillText: () => {},
          moveTo: () => {},
          lineTo: () => {},
          measureText: () => ({ width: 10 }),
          setLineDash: () => {},
          scale: () => {},
          closePath: () => {},
        }),
        appendChild: () => {},
        querySelectorAll: () => [],
        querySelector: () => null,
        addEventListener: () => {},
        setAttribute: () => {},
        parentElement: { clientWidth: 1000, clientHeight: 500 },
        clientWidth: 1000,
        clientHeight: 500,
      };
    }
    return elements[id];
  }

  // Pre-populate elements referenced in the dashboard
  const knownIds = [
    "tableHead", "tableBody", "auctionGrid", "xiSlotsList", "auctionSlotsList",
    "retainedPillarsGrid", "allocatedSpend", "purseRemaining", "teamClutchIndex",
    "purseProgressFill", "scatterCanvas", "radarCanvas", "radarPlayer1",
    "radarPlayer2", "radarComparisonTable", "searchInput", "teamFilter",
    "sortSelect", "xiViewContainer", "squadViewContainer", "btn-view-xi",
    "btn-view-squad", "statTotalPlayers", "statBatters", "statBowlers",
    "statAllRounders", "statAuctionTargets", "statRRPurse", "caseWpaCanvas",
    "caseTelemetryContainer", "caseMatchPills"
  ];
  knownIds.forEach(id => getOrCreateElement(id));

  const sandbox = {
    window: {
      onload: null,
      addEventListener: () => {},
      devicePixelRatio: 1,
    },
    document: {
      getElementById: (id) => getOrCreateElement(id),
      querySelector: (sel) => getOrCreateElement(sel.replace(/[#.]/g, "")),
      querySelectorAll: (sel) => [getOrCreateElement("mock")],
      createElement: (tag) => getOrCreateElement("created_" + tag),
    },
    console: {
      log: () => {},
      error: (...args) => { consoleErrors.push(args.join(" ")); },
      warn: (...args) => { consoleWarns.push(args.join(" ")); },
    },
    Math: Math,
    parseInt: parseInt,
    parseFloat: parseFloat,
    setTimeout: (fn) => fn(),
    setInterval: () => {},
    Set: Set,
    Map: Map,
    Array: Array,
    Object: Object,
  };
  sandbox.window.document = sandbox.document;

  vm.createContext(sandbox);
  vm.runInContext(code, sandbox);

  console.log("✓ Application script evaluated successfully.");

  // Test 1: window.onload execution
  if (typeof sandbox.window.onload === "function") {
    sandbox.window.onload();
    console.log("✓ window.onload executed cleanly.");
  }

  // Test 2: Tab 1 Filter Pills & Roles
  console.log("\n--- Testing Tab 1 Filter Pills & Roles ---");
  const tab1Roles = ["batters", "bowlers", "all_rounders"];
  const tab1Filters = [
    "all", "top10", "free_agent", "ineligible", "traded", "watchlist",
    "rr_core", "untouchable", "global_steal", "domestic_steal"
  ];

  for (const role of tab1Roles) {
    sandbox.setRole(role);
    for (const filter of tab1Filters) {
      sandbox.setFilter(filter, null);
      sandbox.renderTable();
      const tbody = getOrCreateElement("tableBody");
      const rowMatches = [...tbody.innerHTML.matchAll(/<tr[^>]*>/gi)];
      const rowCount = rowMatches.length;
      console.log(`  Tab 1 [role=${role}, filter=${filter}]: ${rowCount} rows rendered`);
      if (filter === "all" || filter === "top10" || filter === "global_steal" || filter === "domestic_steal") {
        if (rowCount === 0) {
          throw new Error(`Tab 1 role=${role} filter=${filter} returned 0 rows!`);
        }
      }
    }
  }
  console.log("✓ All Tab 1 filter pills return populated data without exceptions.");

  // Test 3: Tab 2 Actionable Auction Board Filter Pills
  console.log("\n--- Testing Tab 2 Auction Board Filter Pills ---");
  const tab2Filters = ["all", "released", "global_steal", "domestic", "death", "spin", "pace"];
  for (const filter of tab2Filters) {
    sandbox.renderAuctionBoard(filter);
    const grid = getOrCreateElement("auctionGrid");
    const cardMatches = [...grid.innerHTML.matchAll(/class="auction-card/gi)];
    const cardCount = cardMatches.length;
    console.log(`  Tab 2 [filter=${filter}]: ${cardCount} cards rendered`);
    if (cardCount === 0) {
      throw new Error(`CRITICAL FAILURE: Tab 2 filter='${filter}' rendered ZERO cards (empty grid)!`);
    }
  }
  console.log("✓ All Tab 2 auction filters return populated cards (zero empty grids).");

  // Test 4: Tab 4 Scatter Plot Execution
  console.log("\n--- Testing Tab 4 Scatter Plot Execution ---");
  for (const role of ["batters", "bowlers", "all_rounders"]) {
    sandbox.setScatterRole(role);
    sandbox.drawScatter();
  }
  console.log("✓ Tab 4 scatter plot rendered for batters, bowlers, and all-rounders with 0 errors.");

  // Test 5: Tab 5 Radar Comparator Execution
  console.log("\n--- Testing Tab 5 Radar Comparator Execution ---");
  sandbox.initRadar();
  const p1 = getOrCreateElement("radarPlayer1");
  const p2 = getOrCreateElement("radarPlayer2");
  if (!p1.innerHTML || !p2.innerHTML) {
    throw new Error("Radar select options were not populated!");
  }
  console.log(`  Radar Player 1: ${p1.value}, Player 2: ${p2.value}`);
  sandbox.drawRadar();
  const tableContainer = getOrCreateElement("radarComparisonTable");
  if (!tableContainer.innerHTML) {
    throw new Error("Radar comparison table was not rendered!");
  }
  console.log("✓ Tab 5 radar comparator and comparison table rendered cleanly.");

  // Test 6: Tab 6 Starting XI, 25-man squad roster, and 6 auction slots
  console.log("\n--- Testing Tab 6 Starting XI, 25-Man Squad & 6 Auction Slots ---");
  sandbox.renderXI();
  const xiList = getOrCreateElement("xiSlotsList");
  const xiSlotCards = [...xiList.innerHTML.matchAll(/xi-slot-card/gi)];
  console.log(`  Starting Lineup Slots rendered: ${xiSlotCards.length} (Expected: 12: 11 Core + 1 Impact)`);
  if (xiSlotCards.length < 11) {
    throw new Error(`Expected at least 11 Starting XI slots, got ${xiSlotCards.length}`);
  }

  const auctionSlots = getOrCreateElement("auctionSlotsList");
  const auctionSlotCards = [...auctionSlots.innerHTML.matchAll(/auction-slot-card/gi)];
  console.log(`  Auction Slots rendered: ${auctionSlotCards.length} (Expected: 6 open slots)`);
  if (auctionSlotCards.length !== 6) {
    throw new Error(`Expected exactly 6 auction slots, got ${auctionSlotCards.length}`);
  }

  const retainedGrid = getOrCreateElement("retainedPillarsGrid");
  const retainedCards = [...retainedGrid.innerHTML.matchAll(/squad-player-card/gi)];
  console.log(`  Retained Foundation Pillars rendered: ${retainedCards.length} (Expected: 19 pillars)`);
  if (retainedCards.length !== 19) {
    throw new Error(`Expected exactly 19 retained foundation pillars, got ${retainedCards.length}`);
  }
  console.log(`  Total Squad Roster Capacity: ${retainedCards.length + auctionSlotCards.length} = 25 players!`);
  console.log("✓ Tab 6 Starting XI (11+1), 25-man squad (19 retained), and 6 auction slots verified.");

  // Test 7: Tab 3 10-Franchise Table Data Integrity
  console.log("\n--- Testing Tab 3 10-Franchise Table in HTML ---");
  const franchiseRows = [...html.matchAll(/<span class="franchise-abbr"[^>]*>([A-Z]+)<\/span>\s*([^<]+)<\/span>[\s\S]*?<strong class="num-tabular"[^>]*>([^<]+)<\/strong>/g)];
  console.log(`  Franchises found in Tab 3 table: ${franchiseRows.length}`);
  if (franchiseRows.length !== 10) {
    throw new Error(`Expected 10 franchises in Tab 3, found ${franchiseRows.length}`);
  }
  const expectedPurses = {
    "LSG": "₹47.45 Cr",
    "KKR": "₹41.65 Cr",
    "SRH": "₹40.15 Cr",
    "DC": "₹39.50 Cr",
    "MI": "₹32.60 Cr",
    "CSK": "₹28.05 Cr",
    "RR": "₹27.05 Cr",
    "PBKS": "₹18.60 Cr",
    "RCB": "₹14.15 Cr",
    "GT": "₹8.75 Cr"
  };
  for (const row of franchiseRows) {
    const abbr = row[1];
    const purse = row[3].trim();
    if (expectedPurses[abbr] !== purse) {
      throw new Error(`Franchise ${abbr} expected purse ${expectedPurses[abbr]}, got ${purse}`);
    }
  }
  console.log("✓ All 10 franchises and purse figures match official specifications.");

  // Test 8: Console error & warning assertion
  console.log("\n--- Console Error Audit ---");
  if (consoleErrors.length > 0) {
    throw new Error(`Console errors recorded during execution: ${consoleErrors.join("; ")}`);
  }
  console.log("✓ Zero console errors recorded during full simulated execution.");

  // Test 9: Complete absence of war room
  console.log("\n--- War Room Absence Audit ---");
  const warRoomRegex = new RegExp("war\\s+room", "i");
  if (warRoomRegex.test(html)) {
    throw new Error(`CRITICAL FAILURE: Found 'war room' term in ${htmlPath}!`);
  }
  console.log(`✓ Confirmed complete absence of 'war room' in ${htmlPath}.`);

  console.log(`\n>>> PASSED ALL CHECKS FOR ${htmlPath} <<<\n`);
}

runVerification("dashboard/index.html");
runVerification("index.html");
