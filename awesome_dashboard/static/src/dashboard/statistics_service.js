import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl"

const statisticsService = {
    start() {
        const statistics = reactive({})

        async function loadStatistics(){
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data);
        }

        loadStatistics();
        setInterval(loadStatistics, 1000*10);

        return {
            statistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
