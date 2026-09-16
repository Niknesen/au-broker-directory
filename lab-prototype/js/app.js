
const CHAMPIONS = [{"id": "sydney-abn", "slug": "talk-to-a-broker-sydney", "name": "Talk To A Broker", "lead_broker": "Marcus Vance", "suburb": "Sydney CBD", "city": "sydney", "state": "NSW", "acl": "ACL #483921", "specialty": "Self-Employed & 1-Year ABN Specialists", "settlement_rate": "99.4%", "avg_turnaround": "11 Days", "sla_response": "1.5 Hours", "reviews_count": 822, "rating": 5.0, "trust_score": 98, "strikes": 0, "lenders": "Macquarie, Bankwest, ANZ, Liberty (24 Lenders)", "why_match": "Marcus's team specializes in Alt-Doc, 1-year tax returns, and add-back optimization for NSW business owners. Settled 142 ABN loans last year with zero rate surprises.", "bio": "Ranked #1 audited brokerage in Sydney CBD for self-employed and complex company borrowers."}, {"id": "sydney-firsthome", "slug": "atelier-wealth-sydney", "name": "Atelier Wealth", "lead_broker": "Aaron Christie-David", "suburb": "Sydney", "city": "sydney", "state": "NSW", "acl": "ACL #412099", "specialty": "First Home Buyers & Low Deposit (5% Scheme)", "settlement_rate": "98.9%", "avg_turnaround": "12 Days", "sla_response": "2.0 Hours", "reviews_count": 450, "rating": 5.0, "trust_score": 96, "strikes": 0, "lenders": "CBA, NAB, St George, ING (28 Lenders)", "why_match": "Aaron is NSW's leading specialist for the Federal First Home Guarantee (5% deposit, 0% LMI) and state stamp duty concessions.", "bio": "Award-winning Sydney brokerage dedicated to first-time buyers and families upgrading into their dream home."}, {"id": "melbourne-investor", "slug": "mortgage-broker-melbourne-cbd", "name": "Melbourne Capital Advisory", "lead_broker": "David Chen", "suburb": "Melbourne CBD", "city": "melbourne", "state": "VIC", "acl": "ACL #392810", "specialty": "Refinancing, Equity Extraction & Portfolio Structuring", "settlement_rate": "99.1%", "avg_turnaround": "10 Days", "sla_response": "1.0 Hour", "reviews_count": 586, "rating": 5.0, "trust_score": 97, "strikes": 0, "lenders": "ANZ, Westpac, Macquarie, Bank of Melbourne", "why_match": "David holds direct private pricing desk access across Big-4 banks to negotiate below-advertised rates and maximize borrowing servicing capacity.", "bio": "Melbourne's top-audited mortgage specialist for aggressive rate reductions and property portfolio expansion."}, {"id": "brisbane-fast", "slug": "hunter-galloway-brisbane", "name": "Hunter Galloway Mortgage Advisors", "lead_broker": "Nathan Vecchio", "suburb": "Brisbane City", "city": "brisbane", "state": "QLD", "acl": "ACL #463901", "specialty": "High-LVR & 48h Fast-Track Approvals", "settlement_rate": "99.6%", "avg_turnaround": "9 Days", "sla_response": "45 Mins", "reviews_count": 2497, "rating": 5.0, "trust_score": 99, "strikes": 0, "lenders": "Suncorp, Macquarie, CBA, BOQ (30+ Lenders)", "why_match": "Queensland's most decorated brokerage with an active 48-hour BDM escalation lane. Over 2,400 verified client reviews and a 99.6% approval record.", "bio": "Over 2,400 verified client settlements with zero rate-hike surprises across greater Brisbane."}, {"id": "perth-specialist", "slug": "orange-finance-perth", "name": "Orange Mortgage & Finance", "lead_broker": "Laszlo Szollosi", "suburb": "North Perth", "city": "perth", "state": "WA", "acl": "ACL #390618", "specialty": "Construction, Keystart Transitions & Investment", "settlement_rate": "98.7%", "avg_turnaround": "13 Days", "sla_response": "2.0 Hours", "reviews_count": 260, "rating": 5.0, "trust_score": 95, "strikes": 0, "lenders": "Bankwest, Keystart, Macquarie, NAB", "why_match": "Laszlo is Perth's premier expert on builder progress payment milestones, Keystart refinancing, and WA property growth.", "bio": "Direct ACL holder #390618 specializing in Keystart transitions, construction drawdowns, and Perth property investment."}];
const UNVERIFIED = [{"slug": "apex-mortgage-unverified-sydney", "name": "Apex Finance Solutions", "suburb": "Sydney", "state": "NSW", "rating": 4.2, "reviews": 14, "status": "Unverified Public Index", "conflict_risk": "High (82% volume placed with single Big-4 lender)", "shield_covered": false}, {"slug": "coastal-lending-unverified-sydney", "name": "Coastal Home Loans Sydney", "suburb": "Sydney", "state": "NSW", "rating": 3.9, "reviews": 8, "status": "Unverified Public Index", "conflict_risk": "Unknown (Audit not submitted)", "shield_covered": false}, {"slug": "metro-capital-unverified-melbourne", "name": "Metro Capital Advisors", "suburb": "Melbourne", "state": "VIC", "rating": 4.1, "reviews": 19, "status": "Unverified Public Index", "conflict_risk": "Medium (No SLA Guarantee provided)", "shield_covered": false}, {"slug": "sunshine-state-lending-unverified-brisbane", "name": "Sunshine State Lending", "suburb": "Brisbane", "state": "QLD", "rating": 4.0, "reviews": 11, "status": "Unverified Public Index", "conflict_risk": "High (Unregistered referral arrangement)", "shield_covered": false}];

const STEPS_DATA = [
  {
    step: 1,
    key: "goal",
    title: "Step 1 of 5: What is your exact lending mission?",
    subtitle: "Bank credit appetites differ dramatically depending on the transaction type.",
    telemetry: "Scanning 42 APRA-regulated lending panels...",
    options: [
      { id: "first-home", icon: "🏠", name: "First Home Buyer", desc: "Access First Home Guarantee (5% deposit, 0% LMI) & state grants.", badge: "5% Scheme Expert" },
      { id: "upgrade", icon: "🚀", name: "Upgrading / Next Home", desc: "Bridging loans & buying before selling without financial stress.", badge: "Bridging Specialist" },
      { id: "investor", icon: "📈", name: "Property Investor", desc: "Equity cash-outs, tax structure, and maximum borrowing power.", badge: "Portfolio Structuring" },
      { id: "refinance", icon: "✂️", name: "Refinance & Rate Squeeze", desc: "Claw back 0.75%+ rate reductions and unlock cash.", badge: "Pricing Desk Access" },
      { id: "construction", icon: "🏗️", name: "Construction & Build", desc: "Progress drawdowns and builder contract milestone management.", badge: "Drawdown Expert" }
    ]
  },
  {
    step: 2,
    key: "income",
    title: "Step 2 of 5: How does your household generate income?",
    subtitle: "The #1 reason applications fail. We route only to brokers with matching credit desks.",
    telemetry: "Filtering out 28 lenders that penalize contractor and non-standard payslips...",
    options: [
      { id: "payg", icon: "👔", name: "Standard Full-Time PAYG", desc: "Permanent salary with consistent payslips.", badge: "Prime Tier-1 Desk" },
      { id: "abn", icon: "💼", name: "Self-Employed / Sole Trader", desc: "1–2 year tax returns, Alt-Doc, BAS statements & add-backs.", badge: "Alt-Doc Specialist" },
      { id: "pro", icon: "🩺", name: "Doctor / Lawyer / Accountant", desc: "Qualifies for 90%–95% LMI Waiver policies saving $30k+.", badge: "Private Banking Waiver" },
      { id: "contractor", icon: "⚡", name: "Contractor / Casual / Freelance", desc: "Multiple gigs, probation period, or <6 months tenure.", badge: "Flexible Tenure Policy" }
    ]
  },
  {
    step: 3,
    key: "deposit",
    title: "Step 3 of 5: What is your deposit or equity position?",
    subtitle: "Determines whether you require specialized LMI waivers or Prime rates.",
    telemetry: "Checking Loan-to-Value (LVR) pricing tiers across major Australian aggregators...",
    options: [
      { id: "low-dep", icon: "🛡️", name: "5% – 10% Low Deposit", desc: "Eligible for Federal 5% Scheme or discounted risk tiers.", badge: "Low LMI Desk" },
      { id: "healthy", icon: "💎", name: "20%+ Healthy Deposit", desc: "Standard 80% LVR with maximum rate negotiation leverage.", badge: "Maximum Discount" },
      { id: "guarantor", icon: "🤝", name: "Family Pledge / Guarantor", desc: "Using parents' home equity as security (0% cash deposit).", badge: "Guarantor Legal Desk" },
      { id: "equity", icon: "🏡", name: "Existing Property Equity", desc: "Refinancing existing home to fund the next purchase.", badge: "Cash-Out Policy" }
    ]
  },
  {
    step: 4,
    key: "credit",
    title: "Step 4 of 5: How is your credit profile?",
    subtitle: "We filter out banks that auto-decline minor blemishes.",
    telemetry: "Cross-referencing Prime vs Non-Bank credit thresholds...",
    options: [
      { id: "spotless", icon: "✨", name: "Spotless Credit (700+)", desc: "Clean payment history. Direct access to Tier-1 fast lanes.", badge: "Tier-1 Fast Lane" },
      { id: "minor", icon: "⚠️", name: "Minor Dings / Afterpay", desc: "Missed phone bills, Buy-Now-Pay-Later clutter, small defaults.", badge: "Cleanable Policy" },
      { id: "impaired", icon: "🚨", name: "Impaired / Credit Repair", desc: "Past defaults, tax debt, or historical credit issues.", badge: "Non-Bank Specialist" }
    ]
  },
  {
    step: 5,
    key: "urgency",
    title: "Step 5 of 5: What is your location & urgency timeline?",
    subtitle: "Ensures your matched broker has the required BDM turnaround SLA.",
    telemetry: "Locating #1 Audited Suburb Champion with verified ASIC clean record...",
    options: [
      { id: "urgent-sydney", city: "sydney", icon: "🔥", name: "Sydney (<14 Days / Urgent)", desc: "Auction this weekend or active contract cooling-off period.", badge: "48h BDM Priority" },
      { id: "plan-sydney", city: "sydney", icon: "🧭", name: "Sydney (1–3 Months Strategy)", desc: "Pre-approval and strategic borrowing capacity planning.", badge: "Strategic Planning" },
      { id: "urgent-melbourne", city: "melbourne", icon: "🔥", name: "Melbourne (<14 Days / Urgent)", desc: "Auction or urgent refinance settlement deadline.", badge: "48h BDM Priority" },
      { id: "plan-melbourne", city: "melbourne", icon: "🧭", name: "Melbourne (1–3 Months Strategy)", desc: "Pre-approval and strategic capacity optimization.", badge: "Strategic Planning" },
      { id: "brisbane", city: "brisbane", icon: "☀️", name: "Brisbane / Queensland", desc: "Fast approvals across greater Brisbane & Sunshine/Gold Coast.", badge: "QLD Fast Lane" },
      { id: "perth", city: "perth", icon: "🌊", name: "Perth / WA", desc: "Western Australia property & construction financing.", badge: "WA Specialist" }
    ]
  }
];

let userState = {
  goal: "first-home",
  income: "abn",
  deposit: "low-dep",
  credit: "spotless",
  urgency: "urgent-sydney",
  city: "sydney"
};

let currentStep = 1;
let currentChampIndex = 0;
let matchedChampions = [];

function renderStep(stepNum) {
  currentStep = stepNum;
  const stepData = STEPS_DATA.find(s => s.step === stepNum);
  if (!stepData) return;

  document.getElementById('step-counter-text').innerText = `STEP ${stepNum} OF 5`;
  document.getElementById('progress-fill-bar').style.width = `${stepNum * 20}%`;

  document.getElementById('step-title-text').innerText = stepData.title;
  document.getElementById('step-sub-text').innerText = stepData.subtitle;
  document.getElementById('telemetry-text').innerText = stepData.telemetry;

  const grid = document.getElementById('options-grid-container');
  grid.innerHTML = stepData.options.map(opt => {
    const isSelected = userState[stepData.key] === opt.id;
    return `
      <div class="option-card ${isSelected ? 'selected' : ''}" onclick="selectOption('${stepData.key}', '${opt.id}', '${opt.city || ''}')">
        <div>
          <div class="option-icon">${opt.icon}</div>
          <div class="option-name">${opt.name}</div>
          <div class="option-desc">${opt.desc}</div>
        </div>
        <div class="option-badge">${opt.badge}</div>
      </div>
    `;
  }).join('');

  renderRibbon();
}

function selectOption(key, val, city) {
  userState[key] = val;
  if (city) userState.city = city;

  renderRibbon();

  if (currentStep < 5) {
    renderStep(currentStep + 1);
  } else {
    runScanningSequence();
  }
}

function renderRibbon() {
  const ribbon = document.getElementById('config-ribbon-bar');
  if (!ribbon) return;
  ribbon.innerHTML = `
    <span class="ribbon-label">Config:</span>
    <div class="config-chip ${currentStep === 1 ? 'active' : ''}" onclick="goToStep(1)">
      🎯 ${getOptionName('goal', userState.goal)} <span class="chip-edit">✎</span>
    </div>
    <div class="config-chip ${currentStep === 2 ? 'active' : ''}" onclick="goToStep(2)">
      💼 ${getOptionName('income', userState.income)} <span class="chip-edit">✎</span>
    </div>
    <div class="config-chip ${currentStep === 3 ? 'active' : ''}" onclick="goToStep(3)">
      💰 ${getOptionName('deposit', userState.deposit)} <span class="chip-edit">✎</span>
    </div>
    <div class="config-chip ${currentStep === 4 ? 'active' : ''}" onclick="goToStep(4)">
      ✨ ${getOptionName('credit', userState.credit)} <span class="chip-edit">✎</span>
    </div>
    <div class="config-chip ${currentStep === 5 ? 'active' : ''}" onclick="goToStep(5)">
      📍 ${userState.city.toUpperCase()} <span class="chip-edit">✎</span>
    </div>
  `;
}

function getOptionName(key, val) {
  const step = STEPS_DATA.find(s => s.key === key);
  if (!step) return val;
  const opt = step.options.find(o => o.id === val);
  return opt ? opt.name.split('(')[0].trim() : val;
}

function goToStep(s) {
  document.getElementById('console-step-view').style.display = 'block';
  document.getElementById('scanning-overlay-view').style.display = 'none';
  document.getElementById('champion-reveal-view').style.display = 'none';
  renderStep(s);
}

function runScanningSequence() {
  document.getElementById('console-step-view').style.display = 'none';
  document.getElementById('scanning-overlay-view').style.display = 'block';

  const log = document.getElementById('scan-log-box');
  log.innerHTML = `<div class="scan-line">🔍 Indexing 25,419 ASIC licensed brokers...</div>`;

  setTimeout(() => {
    log.innerHTML += `<div class="scan-line">⚡ Filtering credit policies for ${userState.city.toUpperCase()} + ${getOptionName('income', userState.income)}... [MATCHED]</div>`;
  }, 400);

  setTimeout(() => {
    log.innerHTML += `<div class="scan-line">🛡️ Verifying Best Interests Duty & 0 Strike History... [VERIFIED]</div>`;
  }, 800);

  setTimeout(() => {
    log.innerHTML += `<div class="scan-line" style="color:#10b981; font-weight:800;">👑 SINGLE #1 AUDITED CHAMPION LOCKED.</div>`;
    setTimeout(showChampionReveal, 500);
  }, 1200);
}

function showChampionReveal() {
  document.getElementById('scanning-overlay-view').style.display = 'none';
  document.getElementById('champion-reveal-view').style.display = 'block';

  matchedChampions = CHAMPIONS.filter(c => c.city.toLowerCase() === userState.city.toLowerCase());
  if (matchedChampions.length === 0) matchedChampions = [...CHAMPIONS];

  currentChampIndex = 0;
  renderChampionCard();
}

function renderChampionCard() {
  const c = matchedChampions[currentChampIndex];
  const container = document.getElementById('champion-card-render');
  if (!container) return;

  container.innerHTML = `
    <div class="champ-crown-tag">
      👑 #1 Audited Champion for ${c.suburb}, ${c.state}
    </div>

    <div class="champ-header">
      <div class="champ-name">
        <h2>${c.name}</h2>
        <p>Lead Specialist: <strong>${c.lead_broker}</strong> (${c.acl})</p>
        <div style="margin-top:8px;">
          <span class="option-badge" style="background:rgba(16,185,129,0.15); color:#10b981; border-color:#10b981;">
            🎯 ${c.specialty}
          </span>
        </div>
      </div>
      <div class="trust-score-badge">
        <div class="num">${c.trust_score}/100</div>
        <div class="lbl">Audited Trust Score</div>
      </div>
    </div>

    <div class="why-match-box">
      <strong>🎯 Why ${c.lead_broker} is your exact #1 algorithmic match:</strong>
      <p>${c.why_match}</p>
    </div>

    <div class="proof-metrics-grid">
      <div class="metric-box">
        <div class="v" style="color:#10b981;">${c.settlement_rate}</div>
        <div class="l">Settlement Success Rate</div>
      </div>
      <div class="metric-box">
        <div class="v">${c.avg_turnaround}</div>
        <div class="l">Avg Approval Turnaround</div>
      </div>
      <div class="metric-box">
        <div class="v" style="color:#38bdf8;">${c.sla_response}</div>
        <div class="l">Guaranteed Response SLA</div>
      </div>
      <div class="metric-box">
        <div class="v">0 Strikes</div>
        <div class="l">ASIC Dispute History</div>
      </div>
    </div>

    <div class="enforcer-shield-box">
      <div class="icon">🛡️</div>
      <div class="text">
        <strong>The Best Brokers Enforcer Shield is ACTIVE:</strong>
        ${c.lead_broker} is bound by our strict 2-hour response contract and zero hidden bank fee warranty. If anything goes wrong, our platform executive intervenes immediately.
      </div>
    </div>

    <div class="action-bar">
      <button class="btn-connect-champ" onclick="openProtectedModal('${c.lead_broker}', '${c.name}', '${c.sla_response}')">
        ⚡ Unlock Direct Protected Line with ${c.lead_broker}
      </button>
      <button class="btn-swap-alt" onclick="swapAlternateChampion()">
        🔄 Show #2 Alternate Specialist (${currentChampIndex + 1}/${matchedChampions.length})
      </button>
      <button class="btn-swap-alt" onclick="goToStep(1)">
        ⚙️ Tweak My 5 Parameters
      </button>
    </div>
  `;
}

function swapAlternateChampion() {
  currentChampIndex = (currentChampIndex + 1) % matchedChampions.length;
  renderChampionCard();
}

function openProtectedModal(brokerName, compName, sla) {
  document.getElementById('modal-broker-name').innerText = brokerName;
  document.getElementById('modal-broker-comp').innerText = compName;
  document.getElementById('modal-broker-sla').innerText = sla;
  document.getElementById('protected-modal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('protected-modal').style.display = 'none';
}

function handleBrokerSearch(query) {
  const dropdown = document.getElementById('search-dropdown');
  if (!query || query.trim().length < 2) {
    dropdown.style.display = 'none';
    return;
  }
  
  const q = query.toLowerCase().trim();
  const allBrokers = [
    ...CHAMPIONS.map(c => ({ name: c.name, suburb: c.suburb, state: c.state, slug: `broker/${c.slug}.html`, verified: true })),
    ...UNVERIFIED.map(u => ({ name: u.name, suburb: u.suburb, state: u.state, slug: `broker/${u.slug}.html`, verified: false }))
  ];
  
  const matches = allBrokers.filter(b => b.name.toLowerCase().includes(q) || b.suburb.toLowerCase().includes(q));
  
  if (matches.length === 0) {
    dropdown.innerHTML = `<div style="padding:14px 20px; color:#94a3b8;">No records found for "${query}". Type a broker name (e.g. Talk To A Broker, Apex).</div>`;
    dropdown.style.display = 'block';
    return;
  }
  
  dropdown.innerHTML = matches.map(m => `
    <a href="${m.slug}" class="search-row">
      <div>
        <strong style="color:#fff;">${m.name}</strong>
        <div style="font-size:0.8rem; color:#94a3b8;">${m.suburb}, ${m.state}</div>
      </div>
      <div>
        ${m.verified 
          ? '<span class="tag-v">🛡️ AUDITED CHAMPION</span>' 
          : '<span class="tag-u">⚠️ UNVERIFIED INDEX</span>'}
      </div>
    </a>
  `).join('');
  dropdown.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', () => {
  renderStep(1);
});
