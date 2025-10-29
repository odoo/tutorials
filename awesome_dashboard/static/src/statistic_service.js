/** @odoo-module */

import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const statisticsService = {
    start() {
        const statistics = reactive({})

        async function loadStatistics() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data)
        }

        loadStatistics();
        setInterval(loadStatistics, 10 * 60 * 1000)

        return {
            statistics
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
