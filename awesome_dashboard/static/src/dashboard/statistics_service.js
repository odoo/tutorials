/** @odoo-module **/

import { registry } from "@web/core/registry";

import { reactive } from "@odoo/owl";

const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const stats = reactive({ isReady: false });

        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, updates, { isReady: true });
        }

        setInterval(loadData, 10*60*1000);
        loadData();

        return stats;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
