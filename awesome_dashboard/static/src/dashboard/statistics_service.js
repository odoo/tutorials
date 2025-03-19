import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const data = reactive({isready : false})

        async function loadData(){
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(data, updates, {isReady: true});
        }

        setInterval(loadData, 4*1000);
        loadData();

        return data;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
