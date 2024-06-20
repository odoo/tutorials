/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

export const httpService = {
    dependencies: ["rpc"],
    start(_, { rpc }) {
        const statistics = reactive({
            loaded: false,
        });
        async function loadStatistics() {
            statistics.statistics = await rpc("/awesome_dashboard/statistics");
            statistics.loaded = true;
        }
        setInterval(loadStatistics, 4 * 1000);
        loadStatistics();
        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", httpService);
