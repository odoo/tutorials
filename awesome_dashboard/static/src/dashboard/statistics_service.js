/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const StatisticsService = {
    start() {
        const statistics = reactive({
            isReady: false,
            data: null,  // This will hold your fetched data
        });

        async function loadStatistics() {
            statistics.isReady = false;  // Mark as not ready while loading
            try {
                const response = await rpc("/awesome_dashboard/statistics");
                statistics.data = response;
                statistics.isReady = true;
            } catch (error) {
                console.error("Error fetching statistics:", error);
            }
        }

        loadStatistics();
        setInterval(loadStatistics, 600000);
        return statistics;
    }
};

registry.category("services").add("awesome_dashboard.statistics", StatisticsService);
