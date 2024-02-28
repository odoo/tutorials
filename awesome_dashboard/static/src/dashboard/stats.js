/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

const statistics_service = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        let stats = reactive({});

        async function updateStats() {
            let data = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, data);
        };

        updateStats();
        setInterval(updateStats, 60 * 1000 * 10);

        return {
            load() {
                return stats;
            },
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statistics_service);
