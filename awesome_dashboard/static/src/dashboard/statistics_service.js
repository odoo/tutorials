import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";


const statisticsService = {
    
    start() {
        const result = reactive({ isReady: false });
        

        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(result, updates, { isReady: true });
        }

        setInterval(loadData, 10*60*1000);
        loadData();
        

        return result;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);