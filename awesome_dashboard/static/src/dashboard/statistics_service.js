import {registry} from "@web/core/registry";
import {rpc} from "@web/core/network/rpc";
import {reactive} from "@odoo/owl";


const statisticsService = {

    start() {
        const statistics = reactive({data: []})

        async function refreshData() {
            statistics.data = await rpc("/awesome_dashboard/statistics");
        }

        setInterval(() => refreshData(), 10 * 1000);
        refreshData();
        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
