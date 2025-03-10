import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

const stats_url = "/awesome_dashboard/statistics";
const interval = 100 * 1000; 

const stats = reactive({ dataReady: false });

async function loadStatistics() {
    const result = await rpc(stats_url);
    Object.assign(stats, result, { dataReady: true });
}

function startAutoRefresh() {
    loadStatistics(); 
    setInterval(loadStatistics, interval);
}

const statsService = {
    start() {
        startAutoRefresh();
        return { stats }; 
    }
};

registry.category("services").add("awesome_dashboard.statistics",statsService);
