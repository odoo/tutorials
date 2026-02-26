import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const statisticsService = {

    start() {
        const statistics = reactive({ isReady: false });

        async function loadData() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data, { isReady: true });
        }

        setInterval(loadData, 1000*60*10);
        loadData();

        return statistics;
    },
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
