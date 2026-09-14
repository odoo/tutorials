/** @odoo-module **/
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    name: "awesome_dashboard.statistics",

    start() {
        const stats = reactive({});

        async function loadStatistics() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, data);
        }

        loadStatistics();
        setInterval(loadStatistics, 10 * 60 * 1000);

        return stats;
    },
};

registry
    .category("services")
    .add("awesome_dashboard.statistics", statisticsService);
