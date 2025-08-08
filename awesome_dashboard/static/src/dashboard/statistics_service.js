import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    async: ["loadStatistics"],

    start() {
        const statistics = reactive({ isReady: false });

        async function loadData(params) {
            Object.assign(statistics, await rpc("/awesome_dashboard/statistics"), { isReady: true});
        }

        setInterval(loadData, 10*1000);
        loadData();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
