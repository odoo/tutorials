import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const dashboardStatisticsService = {
    start(env) {
        const statistics = reactive({});

        async function loadData() {
            Object.assign(statistics, await rpc("/awesome_dashboard/statistics"));
        }

        setInterval(loadData, 10 * 60 * 1000);
        loadData();

        return statistics
    },
};

registry.category("services").add("awesome_dashboard.statistics", dashboardStatisticsService);
