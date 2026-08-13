const predictButton = document.getElementById("predictButton");
const backtestButton = document.getElementById("backtestButton");
const clearFiltersButton = document.getElementById("clearFiltersButton");

const rows = document.getElementById("predictionRows");
const statusBox = document.getElementById("status");
const resultSummary = document.getElementById("resultSummary");
const metrics = document.getElementById("metrics");

const positionFilter = document.getElementById("positionFilter");
const teamFilter = document.getElementById("teamFilter");
const playerSearch = document.getElementById("playerSearch");
const minProjection = document.getElementById("minProjection");
const sortBy = document.getElementById("sortBy");
const sortDirection = document.getElementById("sortDirection");

let allPredictions = [];
let loadedSeason = null;
let loadedWeek = null;

function numberValue(id, fallback = 0) {
    const value = Number(document.getElementById(id).value);
    return Number.isFinite(value) ? value : fallback;
}

function setBusy(isBusy) {
    predictButton.disabled = isBusy;
    backtestButton.disabled = isBusy;
}

function setStatus(message, isError = false) {
    statusBox.textContent = message;
    statusBox.className = isError ? "status error" : "status";
}

function getStat(player, name) {
    return Number(player.predicted_stats?.[name] || 0);
}

function getSortValue(player, field) {
    if (field === "passing_yards" ||
        field === "rushing_yards" ||
        field === "receptions" ||
        field === "receiving_yards") {
        return getStat(player, field);
    }

    return player[field] ?? "";
}

function comparePlayers(a, b, field, direction) {
    const aValue = getSortValue(a, field);
    const bValue = getSortValue(b, field);

    let comparison;

    if (typeof aValue === "string" || typeof bValue === "string") {
        comparison = String(aValue).localeCompare(String(bValue));
    } else {
        comparison = Number(aValue) - Number(bValue);
    }

    return direction === "asc" ? comparison : -comparison;
}

function populateTeamFilter() {
    const selectedTeam = teamFilter.value;

    const teams = [...new Set(
        allPredictions
            .map(player => (player.team || "").trim())
            .filter(Boolean)
    )].sort();

    teamFilter.innerHTML = '<option value="ALL">All Teams</option>';

    teams.forEach(team => {
        const option = document.createElement("option");
        option.value = team;
        option.textContent = team;
        teamFilter.appendChild(option);
    });

    if (teams.includes(selectedTeam)) {
        teamFilter.value = selectedTeam;
    }
}

function filteredAndSortedPredictions() {
    const position = positionFilter.value;
    const team = teamFilter.value;
    const search = playerSearch.value.trim().toLowerCase();
    const minimumText = minProjection.value.trim();
    const minimum = minimumText === "" ? null : Number(minimumText);
    const field = sortBy.value;
    const direction = sortDirection.value;

    const filtered = allPredictions.filter(player => {
        if (position !== "ALL" && player.position !== position) {
            return false;
        }

        if (team !== "ALL" && (player.team || "") !== team) {
            return false;
        }

        if (search && !player.player_name.toLowerCase().includes(search)) {
            return false;
        }

        if (minimum !== null &&
            Number.isFinite(minimum) &&
            Number(player.projected_points) < minimum) {
            return false;
        }

        return true;
    });

    return [...filtered].sort(
        (a, b) => comparePlayers(a, b, field, direction)
    );
}

function updateSortHeaders() {
    document.querySelectorAll("th[data-sort]").forEach(th => {
        th.classList.toggle("active-sort", th.dataset.sort === sortBy.value);
    });
}

function renderCurrentView() {
    const items = filteredAndSortedPredictions();

    rows.innerHTML = "";

    if (!items.length) {
        rows.innerHTML =
            '<tr><td colspan="11" class="empty">No players match the current filters.</td></tr>';

        resultSummary.textContent = allPredictions.length
            ? `0 of ${allPredictions.length} loaded players shown`
            : "No projections loaded.";
        updateSortHeaders();
        return;
    }

    items.forEach((player, index) => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${player.player_name}</td>
            <td>${player.team || "-"}</td>
            <td>${player.position}</td>
            <td>${Number(player.projected_points).toFixed(1)}</td>
            <td>${Number(player.low).toFixed(1)}</td>
            <td>${Number(player.high).toFixed(1)}</td>
            <td>${getStat(player, "passing_yards").toFixed(1)}</td>
            <td>${getStat(player, "rushing_yards").toFixed(1)}</td>
            <td>${getStat(player, "receptions").toFixed(1)}</td>
            <td>${getStat(player, "receiving_yards").toFixed(1)}</td>
        `;

        rows.appendChild(tr);
    });

    const weekText = loadedSeason && loadedWeek
        ? ` — ${loadedSeason} Week ${loadedWeek}`
        : "";

    resultSummary.textContent =
        `${items.length} of ${allPredictions.length} loaded players shown${weekText}`;

    updateSortHeaders();
}

async function loadPredictions() {
    const season = numberValue("season");
    const week = numberValue("week");

    setBusy(true);
    metrics.classList.add("hidden");
    setStatus("Loading projections. The model is run only for this season/week request...");

    try {
        // Fetch the complete report once. All filtering and sorting is local after this.
        const response = await fetch(
            `/api/predictions?season=${season}&week=${week}&position=ALL&limit=500`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Prediction request failed.");
        }

        allPredictions = data.predictions;
        loadedSeason = data.season;
        loadedWeek = data.week;

        populateTeamFilter();
        renderCurrentView();

        setStatus(
            `Loaded ${allPredictions.length} projections. ` +
            "Filters and sorting now run instantly in the browser."
        );
    } catch (error) {
        allPredictions = [];
        populateTeamFilter();
        renderCurrentView();
        setStatus(error.message, true);
    } finally {
        setBusy(false);
    }
}

async function runBacktest() {
    const season = numberValue("season");
    const week = numberValue("week");

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

        document.getElementById("mae").textContent = Number(data.mae).toFixed(2);
        document.getElementById("rmse").textContent = Number(data.rmse).toFixed(2);
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

function clearFilters() {
    positionFilter.value = "ALL";
    teamFilter.value = "ALL";
    playerSearch.value = "";
    minProjection.value = "";
    sortBy.value = "projected_points";
    sortDirection.value = "desc";
    renderCurrentView();
}

function sortFromHeader(event) {
    const field = event.currentTarget.dataset.sort;

    if (sortBy.value === field) {
        sortDirection.value =
            sortDirection.value === "desc" ? "asc" : "desc";
    } else {
        sortBy.value = field;

        // Names/team/position are more natural A→Z; numbers default high→low.
        sortDirection.value =
            ["player_name", "team", "position"].includes(field)
                ? "asc"
                : "desc";
    }

    renderCurrentView();
}

predictButton.addEventListener("click", loadPredictions);
backtestButton.addEventListener("click", runBacktest);
clearFiltersButton.addEventListener("click", clearFilters);

[positionFilter, teamFilter, sortBy, sortDirection].forEach(control => {
    control.addEventListener("change", renderCurrentView);
});

[playerSearch, minProjection].forEach(control => {
    control.addEventListener("input", renderCurrentView);
});

document.querySelectorAll("th[data-sort]").forEach(th => {
    th.addEventListener("click", sortFromHeader);
});
