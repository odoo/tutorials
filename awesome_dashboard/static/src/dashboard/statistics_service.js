import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        const statistics = reactive({ data: null });

        const loadStatistics = async () => {
            statistics.data = await rpc("/awesome_dashboard/statistics");
        };

        loadStatistics();

        setInterval(() => {
            loadStatistics();
        }, 10000);

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);