import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start(){
        const statistics = reactive({ isReady: false });
        
        async function getData(){
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        }

        setInterval(getData, 1000*60*10);
        getData();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
