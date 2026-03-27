import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";


export const statisticsService = {
    start() {
        const statistics = reactive({});

        async function fetchStatistics() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data);
        }

        setInterval(fetchStatistics, 5*60*1000);
        fetchStatistics();

        return {statistics};
    },
};

registry.category("services").add("statisticsService", statisticsService);