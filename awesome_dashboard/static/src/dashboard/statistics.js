import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


export const statisticsService = {
    start() {
        const data = reactive({ isReady: false });

        async function loadData(){
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(data, updates, {isReady: true});
        }

        setInterval(loadData, 5000);
        loadData();

        return data;
    }
};

registry.category("services").add("statistics", statisticsService);
