/** @odoo-module */

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {

        // ✅ reactive object
        const statistics = reactive({});

        // ✅ function to fetch data
        async function loadStatistics() {
            const data = await rpc("/awesome_dashboard/statistics");

            // 🔥 update reactive object IN PLACE
            Object.assign(statistics, data);
        }

        // ✅ initial load
        loadStatistics();

        // ✅ auto refresh every 10 sec (testing)
        setInterval(loadStatistics, 10000);

        return {
            statistics,  // 🔥 return reactive object
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);