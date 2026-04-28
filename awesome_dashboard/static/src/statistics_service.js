import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";


export const statisticsService = {
    start() {
        const statistics = reactive({isLoaded: false});

        async function loadStatistics() {
            Object.assign(statistics, await rpc("/awesome_dashboard/statistics"), {isLoaded: true});
        }

        setInterval(loadStatistics, 10 * 60 * 1000);
        loadStatistics();

        return {
            loadStatistics: statistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
