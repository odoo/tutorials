import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const REFRESH_INTERVAL = 10_000;

const statisticsService = {
    async start() {
        const statistics = reactive({
            data: [],
        });

        async function loadStatistics() {
            const newStatistics = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, newStatistics);
        }

        await loadStatistics();
        setInterval(loadStatistics, REFRESH_INTERVAL);

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
