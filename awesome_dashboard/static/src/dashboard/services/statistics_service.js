import { reactive } from "@odoo/owl";

const REFRESH_INTERVAL = 10000; // make it 600000 for 10mins

export const statisticsStore = reactive({
    data: null,
    isReady: false,
});

async function loadStatistics() {
    const response = await fetch("/awesome_dashboard/statistics", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jsonrpc: "2.0", method: "call", params: {}, id: Date.now() }),
    });
    const payload = await response.json();
    statisticsStore.data = payload.result;
    statisticsStore.isReady = true;
}

// Initial load
loadStatistics();

// Auto-refresh
setInterval(loadStatistics, REFRESH_INTERVAL);