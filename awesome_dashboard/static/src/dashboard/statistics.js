import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const data = reactive({});

async function loadStatistics() {
    try {
        const result = await rpc("/awesome_dashboard/statistics");
        Object.assign(data, result);
    } catch (error) {
        console.error("Failed to load statistics:", error);
    }
}

setInterval(loadStatistics, 10 * 1000);

export const statisticsService = {
    start() {
        return { data, loadStatistics };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
