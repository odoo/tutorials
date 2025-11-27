import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const statistics = reactive({
            orders_by_size: {},
        });

        async function loadData() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data);
        }

        setInterval(loadData, 10000);
        loadData();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
