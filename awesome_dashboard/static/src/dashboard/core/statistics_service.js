/** @odoo-module */

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({ isReady: false });
        async function loadData() {
            const updates =  await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true })
        }
        const TEN_MIN = 10 * 60 * 1000;
        setInterval(loadData, TEN_MIN);
        loadData();
        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
