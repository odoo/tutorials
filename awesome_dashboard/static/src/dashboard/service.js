import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


const Statistics = {
    start() {
        const statistics = reactive({ isReady: false });

        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        }

        setInterval(loadData, 1000 * 60 * 10);
        loadData();

        return statistics;
    },
};


registry.category("services").add("awesome_dashboard.statistics", Statistics);
