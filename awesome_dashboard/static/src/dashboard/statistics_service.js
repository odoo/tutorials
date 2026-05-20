import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const statisticsService = {
    start() {
        const statistics = reactive({});

        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates);
        }

        setInterval(loadData, 600000);
        loadData();
        return { statistics };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
