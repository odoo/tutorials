import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


export const statisticsService = {
    start() {
        const statistics = reactive({});

        async function loadStatistics() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data);
        }

        loadStatistics();

        setInterval(() => {
            loadStatistics();
        }, 10000);

        return {
            statistics,
        };

    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);