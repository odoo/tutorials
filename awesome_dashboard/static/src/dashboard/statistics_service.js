import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    dependencies: [],
    start() {
        const stats = reactive({});

        const loadStatistics = async () => {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, data);
        };
        setInterval(loadStatistics, 10000);
        loadStatistics();

        return {
            stats,
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
