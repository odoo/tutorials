import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statistics = reactive({
    data: {},
});

async function loadStatistics() {
    try {
        const result = await rpc("/awesome_dashboard/statistics");
        console.log("API Result:", result);

        if (result) {
            statistics.data = result;;
        }
    } catch (error) {
        console.error("Error loading stats:", error);
    }
}

export const statisticsService = {
    start() {

        loadStatistics();

        setInterval(loadStatistics, 10000);

        return {
            statistics,
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);