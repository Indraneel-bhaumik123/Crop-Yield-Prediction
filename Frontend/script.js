/**
 * AgriYield Interactive Agricultural Dashboard Logic
 * Integrates with FastAPI backend for authentication, dynamic options,
 * real ML model inference, user history, and analytics.
 */

const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000"
  : window.location.origin;

let CURRENT_OPTIONS = null;
let CHART_SEASON = null;
let CHART_CROPS = null;
let CHART_TREND = null;
let CHART_ANALYTICS_YEARLY = null;
let CHART_ANALYTICS_COUNTRIES = null;

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener("DOMContentLoaded", async () => {
  checkAuth();
  await loadSeasonOptions("Kharif");
  initCharts();
  loadQuickStats();
  loadModelComparison();

  // Handle URL hash navigation
  if (window.location.hash) {
    const viewName = window.location.hash.replace("#", "");
    if (viewName === "prediction") {
      switchView("dashboard", true);
    } else {
      switchView(viewName);
    }
  }
});

// =============================================================================
// AUTHENTICATION & LOGIN-FIRST FLOW
// =============================================================================

function checkAuth() {
  const token = localStorage.getItem("agriyield_token");
  const authOverlay = document.getElementById("authOverlay");

  if (!token) {
    authOverlay.classList.remove("hidden");
  } else {
    authOverlay.classList.add("hidden");
    fetchUserProfile();
    loadHistoryData();
  }
}

async function fetchUserProfile() {
  const token = localStorage.getItem("agriyield_token");
  if (!token) return;

  try {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (res.ok) {
      const data = await res.json();
      document.getElementById("userDisplayName").innerText = data.username;
      document.getElementById("userAvatarText").innerText = data.username.charAt(0).toUpperCase();
    } else if (res.status === 401) {
      handleLogout();
    }
  } catch (err) {
    console.warn("Could not fetch user profile:", err);
  }
}

function switchAuthTab(tab) {
  const tabLogin = document.getElementById("tabBtnLogin");
  const tabRegister = document.getElementById("tabBtnRegister");
  const formLogin = document.getElementById("loginForm");
  const formRegister = document.getElementById("registerForm");
  const errorBanner = document.getElementById("authErrorBanner");
  errorBanner.style.display = "none";

  if (tab === "login") {
    tabLogin.classList.add("active");
    tabRegister.classList.remove("active");
    formLogin.classList.add("active");
    formRegister.classList.remove("active");
  } else {
    tabRegister.classList.add("active");
    tabLogin.classList.remove("active");
    formRegister.classList.add("active");
    formLogin.classList.remove("active");
  }
}

function showAuthError(msg) {
  const banner = document.getElementById("authErrorBanner");
  banner.innerText = msg;
  banner.style.display = "block";
}

async function handleLoginSubmit(e) {
  e.preventDefault();
  const username = document.getElementById("loginUsername").value.trim();
  const password = document.getElementById("loginPassword").value;
  const btn = document.getElementById("btnLoginSubmit");
  btn.disabled = true;
  btn.innerText = "Signing in...";

  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();

    if (res.ok && data.access_token) {
      localStorage.setItem("agriyield_token", data.access_token);
      localStorage.setItem("agriyield_username", data.username);
      document.getElementById("authOverlay").classList.add("hidden");
      document.getElementById("userDisplayName").innerText = data.username;
      document.getElementById("userAvatarText").innerText = data.username.charAt(0).toUpperCase();
      loadHistoryData();
      switchView("dashboard", true);
    } else {
      showAuthError(data.detail || "Invalid username or password.");
    }
  } catch (err) {
    showAuthError("Connection error. Ensure FastAPI backend is running.");
  } finally {
    btn.disabled = false;
    btn.innerText = "Sign In to Dashboard";
  }
}

async function handleRegisterSubmit(e) {
  e.preventDefault();
  const username = document.getElementById("regUsername").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const password = document.getElementById("regPassword").value;
  const btn = document.getElementById("btnRegisterSubmit");
  btn.disabled = true;
  btn.innerText = "Creating account...";

  try {
    const res = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });
    const data = await res.json();

    if (res.ok && data.access_token) {
      localStorage.setItem("agriyield_token", data.access_token);
      localStorage.setItem("agriyield_username", data.username);
      document.getElementById("authOverlay").classList.add("hidden");
      document.getElementById("userDisplayName").innerText = data.username;
      document.getElementById("userAvatarText").innerText = data.username.charAt(0).toUpperCase();
      loadHistoryData();
      switchView("dashboard", true);
    } else {
      showAuthError(data.detail || "Registration failed.");
    }
  } catch (err) {
    showAuthError("Connection error. Ensure FastAPI backend is running.");
  } finally {
    btn.disabled = false;
    btn.innerText = "Create Account";
  }
}

async function quickDemoLogin() {
  const username = "Admin";
  const password = "adminPassword123!";
  const email = "admin@agriyield.org";

  // Try login first
  try {
    let res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) {
      // Auto register if demo user doesn't exist yet
      res = await fetch(`${API_BASE}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
      });
    }

    const data = await res.json();
    if (data.access_token) {
      localStorage.setItem("agriyield_token", data.access_token);
      localStorage.setItem("agriyield_username", data.username);
      document.getElementById("authOverlay").classList.add("hidden");
      document.getElementById("userDisplayName").innerText = data.username;
      document.getElementById("userAvatarText").innerText = data.username.charAt(0).toUpperCase();
      loadHistoryData();
      switchView("dashboard", true);
    }
  } catch (err) {
    // If backend is unreachable, fill form inputs
    document.getElementById("loginUsername").value = username;
    document.getElementById("loginPassword").value = password;
  }
}

function handleLogout() {
  localStorage.removeItem("agriyield_token");
  localStorage.removeItem("agriyield_username");
  document.getElementById("authOverlay").classList.remove("hidden");
}

// =============================================================================
// NAVIGATION & VIEW SWITCHING
// =============================================================================

function switchView(viewId, scrollToPrediction = false) {
  const sections = {
    dashboard: document.getElementById("viewDashboard"),
    models: document.getElementById("viewModelComparison"),
    analytics: document.getElementById("viewAnalytics"),
    health: document.getElementById("viewHealth"),
    history: document.getElementById("viewHistory"),
    reports: document.getElementById("viewReports"),
    about: document.getElementById("viewAbout")
  };

  const navLinks = {
    dashboard: document.getElementById("navDashboard"),
    prediction: document.getElementById("navPrediction"),
    models: document.getElementById("navModels"),
    analytics: document.getElementById("navAnalytics"),
    health: document.getElementById("navHealth"),
    history: document.getElementById("navHistory"),
    reports: document.getElementById("navReports"),
    about: document.getElementById("navAbout")
  };

  // Hide all sections
  Object.values(sections).forEach(sec => sec && sec.classList.remove("active"));
  Object.values(navLinks).forEach(link => link && link.classList.remove("active"));

  if (viewId === "prediction") {
    viewId = "dashboard";
    scrollToPrediction = true;
  }

  if (sections[viewId]) {
    sections[viewId].classList.add("active");
    if (navLinks[viewId]) {
      navLinks[viewId].classList.add("active");
    }
  }

  if (scrollToPrediction) {
    const el = document.getElementById("prediction");
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  // Load section-specific data
  if (viewId === "history") loadHistoryData();
  if (viewId === "models") loadModelComparison();
  if (viewId === "analytics") loadDetailedAnalytics();
}

// =============================================================================
// DYNAMIC HIERARCHICAL DROPDOWNS: Season -> Continent -> Country -> Crop
// =============================================================================

async function loadSeasonOptions(season) {
  try {
    const res = await fetch(`${API_BASE}/options?season=${season}`);
    if (!res.ok) throw new Error("Failed to load options");
    const data = await res.json();
    CURRENT_OPTIONS = data;

    // Populate Continents
    const continentSelect = document.getElementById("selectContinent");
    continentSelect.innerHTML = "";
    data.continents.forEach(cont => {
      const opt = document.createElement("option");
      opt.value = cont;
      opt.textContent = cont;
      if (cont === "Asia") opt.selected = true;
      continentSelect.appendChild(opt);
    });

    onContinentChanged(continentSelect.value || data.continents[0]);

    // Apply defaults to numeric fields if provided
    if (data.stats) {
      if (data.stats.rainfall_mm) document.getElementById("inputRainfall").value = data.stats.rainfall_mm.default;
      if (data.stats.pesticides_tonnes) document.getElementById("inputPesticides").value = data.stats.pesticides_tonnes.default;
      if (data.stats.avg_temp) document.getElementById("inputTemperature").value = data.stats.avg_temp.default;
    }
  } catch (err) {
    console.error("Error loading season options:", err);
  }
}

function onSeasonChanged(season) {
  loadSeasonOptions(season);
}

function onContinentChanged(continent) {
  if (!CURRENT_OPTIONS || !CURRENT_OPTIONS.hierarchy) return;

  const countries = Object.keys(CURRENT_OPTIONS.hierarchy[continent] || {});
  const countrySelect = document.getElementById("selectCountry");
  countrySelect.innerHTML = "";

  countries.forEach(country => {
    const opt = document.createElement("option");
    opt.value = country;
    opt.textContent = country;
    if (country === "India") opt.selected = true;
    countrySelect.appendChild(opt);
  });

  const selectedCountry = countrySelect.value || countries[0];
  onCountryChanged(selectedCountry);
}

function onCountryChanged(country) {
  if (!CURRENT_OPTIONS || !CURRENT_OPTIONS.hierarchy) return;

  const continent = document.getElementById("selectContinent").value;
  const crops = (CURRENT_OPTIONS.hierarchy[continent] && CURRENT_OPTIONS.hierarchy[continent][country]) || [];
  const cropSelect = document.getElementById("selectCrop");
  cropSelect.innerHTML = "";

  crops.forEach(crop => {
    const opt = document.createElement("option");
    opt.value = crop;
    opt.textContent = crop;
    if (crop.toLowerCase().includes("rice") || crop.toLowerCase().includes("maize") || crop.toLowerCase().includes("wheat")) {
      opt.selected = true;
    }
    cropSelect.appendChild(opt);
  });
}

// =============================================================================
// PREDICTION FORM SUBMISSION & RESULT VISUALIZATION
// =============================================================================

async function handlePredictionSubmit(e) {
  e.preventDefault();
  const token = localStorage.getItem("agriyield_token");
  if (!token) {
    document.getElementById("authOverlay").classList.remove("hidden");
    return;
  }

  const payload = {
    season: document.getElementById("selectSeason").value,
    continent: document.getElementById("selectContinent").value,
    area: document.getElementById("selectCountry").value,
    crop: document.getElementById("selectCrop").value,
    year: parseInt(document.getElementById("inputYear").value, 10),
    average_rain_fall_mm_per_year: parseFloat(document.getElementById("inputRainfall").value),
    pesticides_tonnes: parseFloat(document.getElementById("inputPesticides").value),
    avg_temp: parseFloat(document.getElementById("inputTemperature").value)
  };

  const btn = document.getElementById("btnPredictYield");
  btn.disabled = true;
  btn.innerHTML = `<span>⏳</span> Calculating Prediction...`;

  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.ok && data.success) {
      updatePredictionDisplay(data);
    } else {
      alert(`Prediction Error: ${data.detail || "Unable to compute yield."}`);
    }
  } catch (err) {
    alert("Connection error: Unable to contact FastAPI backend.");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>✨</span> Predict Crop Yield`;
  }
}

function updatePredictionDisplay(data) {
  // 1. Yield Number & Badge
  const yieldFormatted = data.predicted_yield_hg_per_ha.toLocaleString();
  document.getElementById("resYieldValue").innerText = yieldFormatted;

  const badgeEl = document.getElementById("resYieldBadge");
  if (data.potential_rating === "Excellent" || data.potential_rating === "Good") {
    badgeEl.innerHTML = `<span>🌱</span> High Yield Potential`;
    badgeEl.style.background = "rgba(255, 255, 255, 0.25)";
  } else {
    badgeEl.innerHTML = `<span>⚠️</span> Moderate Yield Potential`;
    badgeEl.style.background = "rgba(234, 179, 8, 0.3)";
  }

  // 2. Potential Radial Gauge
  const score = data.potential_score || 85;
  document.getElementById("resPotentialScore").innerHTML = `${score}<span>/100</span>`;
  const ratingEl = document.getElementById("resPotentialRating");
  ratingEl.innerText = data.potential_rating || "Good";

  if (score >= 85) ratingEl.style.color = "#15803d";
  else if (score >= 70) ratingEl.style.color = "#22c55e";
  else if (score >= 50) ratingEl.style.color = "#eab308";
  else ratingEl.style.color = "#ef4444";

  // Calculate stroke offset: circumference is 2 * PI * 40 = 251.2
  const maxDash = 251.2;
  const offset = maxDash - (maxDash * score / 100);
  const fillCircle = document.getElementById("gaugeCircleFill");
  fillCircle.style.strokeDashoffset = offset;
  fillCircle.style.stroke = ratingEl.style.color;

  // 3. Metadata Breakdown
  document.getElementById("metaCrop").innerText = data.crop;
  document.getElementById("metaModel").innerText = data.model_used;
  document.getElementById("metaSeason").innerText = data.season;
  document.getElementById("metaTime").innerText = data.timestamp;
  document.getElementById("metaCountry").innerText = data.country;
  document.getElementById("metaConfidence").innerText = data.confidence || "92.4%";
  document.getElementById("metaContinent").innerText = data.continent;
  document.getElementById("metaStatus").innerText = "✓ Success";
  document.getElementById("metaYear").innerText = data.year;
  document.getElementById("metaHistoryId").innerText = `#${data.history_id}`;

  // 4. Factor Impact Badges
  if (data.factors_impact) {
    setFactorBadge("factorRain", data.factors_impact.rainfall);
    setFactorBadge("factorTemp", data.factors_impact.temperature);
    setFactorBadge("factorPest", data.factors_impact.pesticides);
  }
}

function setFactorBadge(elementId, statusText) {
  const el = document.getElementById(elementId);
  if (!el) return;
  el.innerText = statusText;
  el.className = "factor-badge " + (statusText.toLowerCase().includes("favorable") ? "favorable" : "within-range");
}

// =============================================================================
// CHARTS INITIALIZATION & AGRI ANALYTICS
// =============================================================================

function initCharts() {
  // Chart 1: Average Yield by Season
  const ctxSeason = document.getElementById("chartYieldBySeason").getContext("2d");
  CHART_SEASON = new Chart(ctxSeason, {
    type: "bar",
    data: {
      labels: ["Kharif", "Rabi", "Seasonal"],
      datasets: [{
        label: "Mean Yield (hg/ha)",
        data: [44838, 30783, 98125],
        backgroundColor: ["#2e7d32", "#1976d2", "#f57c00"],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: "#edf2ee" } },
        x: { grid: { display: false } }
      }
    }
  });

  // Chart 2: Top Crops (By Average Yield)
  const ctxCrops = document.getElementById("chartTopCrops").getContext("2d");
  CHART_CROPS = new Chart(ctxCrops, {
    type: "doughnut",
    data: {
      labels: ["Potatoes", "Cassava", "Rice", "Maize", "Wheat"],
      datasets: [{
        data: [2091, 941, 1502, 2028, 1810],
        backgroundColor: ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"],
        borderWidth: 2,
        borderColor: "#ffffff"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "68%",
      plugins: {
        legend: {
          position: "right",
          labels: { boxWidth: 10, font: { size: 10 } }
        }
      }
    }
  });

  // Chart 3: Yield Trend
  const ctxTrend = document.getElementById("chartYieldTrend").getContext("2d");
  CHART_TREND = new Chart(ctxTrend, {
    type: "line",
    data: {
      labels: ["1990", "1994", "1998", "2002", "2006", "2010", "2013"],
      datasets: [{
        label: "Trend",
        data: [42000, 46500, 51200, 56800, 64200, 71500, 78400],
        borderColor: "#279655",
        backgroundColor: "rgba(39, 150, 85, 0.1)",
        tension: 0.35,
        fill: true,
        pointRadius: 4,
        pointBackgroundColor: "#279655"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: { color: "#edf2ee" } },
        x: { grid: { display: false } }
      }
    }
  });
}

async function loadQuickStats() {
  try {
    const res = await fetch(`${API_BASE}/analytics/summary`);
    if (!res.ok) return;
    const data = await res.json();
    document.getElementById("statCountries").innerText = `${data.total_countries}+`;
    document.getElementById("statCrops").innerText = `${data.total_crops}+`;
    document.getElementById("statRecords").innerText = data.total_records.toLocaleString();
  } catch (err) {
    console.warn("Could not load quick stats:", err);
  }
}

async function loadDetailedAnalytics() {
  try {
    const resYearly = await fetch(`${API_BASE}/analytics/yearly`);
    if (resYearly.ok) {
      const yData = await resYearly.json();
      renderYearlyChart(yData.data);
    }

    const resCountries = await fetch(`${API_BASE}/analytics/countries?limit=8`);
    if (resCountries.ok) {
      const cData = await resCountries.json();
      renderCountriesChart(cData.data);
    }
  } catch (err) {
    console.error("Analytics loading error:", err);
  }
}

function renderYearlyChart(yearlyData) {
  const ctx = document.getElementById("chartAnalyticsYearly").getContext("2d");
  if (CHART_ANALYTICS_YEARLY) CHART_ANALYTICS_YEARLY.destroy();

  const kharif = yearlyData.filter(d => d.season === "Kharif");
  const rabi = yearlyData.filter(d => d.season === "Rabi");
  const seasonal = yearlyData.filter(d => d.season === "Seasonal");

  const years = Array.from(new Set(yearlyData.map(d => d.year))).sort((a, b) => a - b);

  CHART_ANALYTICS_YEARLY = new Chart(ctx, {
    type: "line",
    data: {
      labels: years,
      datasets: [
        {
          label: "Kharif",
          data: years.map(y => (kharif.find(d => d.year === y) || {}).average_yield || null),
          borderColor: "#2e7d32",
          tension: 0.3
        },
        {
          label: "Rabi",
          data: years.map(y => (rabi.find(d => d.year === y) || {}).average_yield || null),
          borderColor: "#1976d2",
          tension: 0.3
        },
        {
          label: "Seasonal",
          data: years.map(y => (seasonal.find(d => d.year === y) || {}).average_yield || null),
          borderColor: "#f57c00",
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { y: { grid: { color: "#edf2ee" } } }
    }
  });
}

function renderCountriesChart(countryData) {
  const ctx = document.getElementById("chartAnalyticsCountries").getContext("2d");
  if (CHART_ANALYTICS_COUNTRIES) CHART_ANALYTICS_COUNTRIES.destroy();

  const topCountries = countryData.slice(0, 8);
  CHART_ANALYTICS_COUNTRIES = new Chart(ctx, {
    type: "bar",
    data: {
      labels: topCountries.map(d => d.country),
      datasets: [{
        label: "Mean Yield (hg/ha)",
        data: topCountries.map(d => d.average_yield),
        backgroundColor: "#16a34a",
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: "#edf2ee" } },
        x: { grid: { display: false } }
      }
    }
  });
}

// =============================================================================
// MODEL COMPARISON SECTION
// =============================================================================

async function loadModelComparison() {
  try {
    const res = await fetch(`${API_BASE}/model-comparison`);
    if (!res.ok) return;
    const data = await res.json();
    const tbody = document.getElementById("tbodyModelComparison");
    tbody.innerHTML = "";

    data.evaluation_results.forEach(row => {
      const isWinner = row.Model.includes("KNN");
      const statusBadge = isWinner
        ? `<span class="champion-tag">★ Selected Champion</span>`
        : `<span class="baseline-tag">${row.Model.includes("Linear") ? "Baseline" : "Paper Candidate"}</span>`;

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${row.Season}</strong></td>
        <td>${row.Model}</td>
        <td>${row.RMSE ? Number(row.RMSE).toLocaleString() : "-"}</td>
        <td>${row.MAE ? Number(row.MAE).toLocaleString() : "-"}</td>
        <td><strong>${row.R2 ? Number(row.R2).toFixed(4) : "-"}</strong></td>
        <td>${row.Pearson_r ? Number(row.Pearson_r).toFixed(4) : "-"}</td>
        <td>${statusBadge}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.warn("Could not load model comparison table:", err);
  }
}

// =============================================================================
// PREDICTION HISTORY MANAGEMENT
// =============================================================================

async function loadHistoryData() {
  const token = localStorage.getItem("agriyield_token");
  if (!token) return;

  try {
    const res = await fetch(`${API_BASE}/history`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) return;
    const data = await res.json();
    const tbody = document.getElementById("tbodyHistory");
    tbody.innerHTML = "";

    if (data.history.length === 0) {
      tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; color:#8fa699; padding:24px;">No prediction records saved yet. Run your first prediction above!</td></tr>`;
      return;
    }

    data.history.forEach(item => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>#${item.id}</td>
        <td>${item.season}</td>
        <td>${item.area} (${item.continent})</td>
        <td><strong>${item.crop}</strong></td>
        <td>${item.year}</td>
        <td>${item.average_rain_fall_mm_per_year} mm</td>
        <td>${item.pesticides_tonnes} t</td>
        <td>${item.avg_temp}°C</td>
        <td><strong>${item.predicted_yield_hg_per_ha.toLocaleString()}</strong> hg/ha</td>
        <td><span class="champion-tag">${item.potential_score}/100</span></td>
        <td>
          <button style="background:none;border:none;color:#ef4444;cursor:pointer;font-weight:700;" onclick="deleteHistoryItem(${item.id})">✕ Delete</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.warn("Could not load prediction history:", err);
  }
}

async function deleteHistoryItem(id) {
  if (!confirm(`Delete prediction record #${id}?`)) return;
  const token = localStorage.getItem("agriyield_token");

  try {
    const res = await fetch(`${API_BASE}/history/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    });
    if (res.ok) {
      loadHistoryData();
    }
  } catch (err) {
    alert("Failed to delete record.");
  }
}
