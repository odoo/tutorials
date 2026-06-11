import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const REFRESH_INTERVAL = 10 * 1000; // 10 seconds for testing (use 10 * 60 * 1000 for 10 min)

const statisticsService = {
    start() {
        const statistics = reactive({});

        async function loadStatistics() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data);
        }

        loadStatistics();
        setInterval(loadStatistics, REFRESH_INTERVAL);

        return { statistics };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
