const seasonInput = document.getElementById("season");
const weekInput = document.getElementById("week");
const positionInput = document.getElementById("position");
const predictButton = document.getElementById("predictButton");
const backtestButton = document.getElementById("backtestButton");
const rows = document.getElementById("predictionRows");
const statusBox = document.getElementById("status");
const resultSummary = document.getElementById("resultSummary");
const playerSearch = document.getElementById("playerSearch");
const metrics = document.getElementById("metrics");

let currentPredictions = [];

function value(id, fallback = 0) {
    const v = Number(document.getElementById(id).value);
    return Number.isFinite(v) ? v : fallback;
}

function setBusy(isBusy) {
    predictButton.disabled = isBusy;
    backtestButton.disabled = isBusy;
}

function setStatus(message, isError = false) {
    statusBox.textContent = message;
    statusBox.className = isError ? "status error" : "status";
}

function stat(player, name) {
    return Number(player.predicted_stats?.[name] || 0).toFixed(1);
}

function renderPredictions(items) {
    rows.innerHTML = "";

    if (!items.length) {
        rows.innerHTML = '<tr><td colspan="10" class="empty">No matching players.</td></tr>';
        return;
    }

    items.forEach((player, index) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${player.player_name}</td>
            <td>${player.position}</td>
            <td>${player.projected_points.toFixed(1)}</td>
            <td>${player.low.toFixed(1)}</td>
            <td>${player.high.toFixed(1)}</td>
            <td>${stat(player, "passing_yards")}</td>
            <td>${stat(player, "rushing_yards")}</td>
            <td>${stat(player, "receptions")}</td>
            <td>${stat(player, "receiving_yards")}</td>
        `;
        rows.appendChild(tr);
    });
}

async function generatePredictions() {
    const season = value("season");
    const week = value("week");
    const position = positionInput.value;

    setBusy(true);
    metrics.classList.add("hidden");
    setStatus("Downloading data, training models and generating projections...");

    try {
        const url =
            `/api/predictions?season=${season}&week=${week}` +
            `&position=${encodeURIComponent(position)}&limit=200`;

        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Prediction request failed.");
        }

        currentPredictions = data.predictions;
        renderPredictions(currentPredictions);

        resultSummary.textContent =
            `${data.count} players — ${data.season} Week ${data.week}`;
        setStatus("Projection complete.");
    } catch (error) {
        setStatus(error.message, true);
    } finally {
        setBusy(false);
    }
}

async function runBacktest() {
    const season = value("season");
    const week = value("week");

    setBusy(true);
    setStatus("Running historical backtest...");

    try {
        const response = await fetch(
            `/api/backtest?season=${season}&week=${week}`
        );
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Backtest failed.");
        }

        document.getElementById("mae").textContent = data.mae.toFixed(2);
        document.getElementById("rmse").textContent = data.rmse.toFixed(2);
        document.getElementById("within2").textContent = `${data.within_2}%`;
        document.getElementById("within4").textContent = `${data.within_4}%`;
        document.getElementById("within6").textContent = `${data.within_6}%`;

        metrics.classList.remove("hidden");
        setStatus(`Backtest complete for ${season} Week ${week}.`);
    } catch (error) {
        setStatus(error.message, true);
    } finally {
        setBusy(false);
    }
}

playerSearch.addEventListener("input", () => {
    const query = playerSearch.value.toLowerCase().trim();

    const filtered = currentPredictions.filter(player =>
        player.player_name.toLowerCase().includes(query)
    );

    renderPredictions(filtered);
});

predictButton.addEventListener("click", generatePredictions);
backtestButton.addEventListener("click", runBacktest);
