import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticService = {
    start() {
        const statistics = reactive({debounce: false});

        async function loadStatistics() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, {debounce: true});
        }

        setInterval(loadStatistics, 5 * 1000);
        loadStatistics();

        return statistics;
    }
};

registry.category("services").add("awesome_dashboard.statistics", statisticService);
