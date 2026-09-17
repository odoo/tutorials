import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import {reactive} from "@odoo/owl";

export const statisticsService = {
    dependencies: [],
    start() {
        const stats = reactive({});
        async function loadData(){
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, data);
        }
        loadData();
        setInterval(loadData, 10000);
        return stats;
    }
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService);