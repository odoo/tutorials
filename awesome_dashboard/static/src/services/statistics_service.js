import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    dependencies: [],

    start(_env) {
        const statistics = reactive({ isReady: false });
        const loadData = async () => {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        };

        setInterval(loadData, 3 * 1000);
        loadData();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
