import {registry} from "@web/core/registry";
import {rpc} from "@web/core/network/rpc";
import {reactive} from "@odoo/owl";

const statisticsService = {
    start() {
        const stats = reactive({isReady: false});

        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, updates, {isReady: true});
        }

        setInterval(loadData, 10 * 60 * 1000);
        loadData();
        return stats;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
