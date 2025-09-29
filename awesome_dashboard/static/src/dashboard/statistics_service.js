import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const statistics = reactive({isReady : false});
        async function loadingData() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data, {isReady : true});
        }
        loadingData();
        setInterval(loadingData, 1000 * 60 * 10);
        return statistics;
    },
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
