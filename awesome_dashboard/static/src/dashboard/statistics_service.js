/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

export const statistics = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        let statistics = reactive({'data': {}});

        const loadStatistics = async function getStatistics() {
            const data = await rpc("/awesome_dashboard/statistics");
            statistics.data = data;
        };

        loadStatistics();
        setInterval(loadStatistics, 5000);

        return {
            statistics
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statistics);
