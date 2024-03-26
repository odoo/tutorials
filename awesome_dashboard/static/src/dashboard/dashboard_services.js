/** @odoo-module */

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const getDashboardStatistics = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({ isRefresh: false });

        async function fetchData() {
            const results = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, results, { isRefresh: true });
        }
        
        setInterval(fetchData, 10*1000);
        fetchData();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", getDashboardStatistics);