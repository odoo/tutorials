import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statistics = reactive({});

async function loadStatistics() {
    const data = await rpc("/awesome_dashboard/statistics");
    Object.assign(statistics, data);
}

export const statisticsService = {
    start() {
        loadStatistics();
        setInterval(loadStatistics, 10000);
        return statistics;
    },
};

registry.category("services").add("statistics", statisticsService);
