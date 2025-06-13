import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

registry.category("services").add("awesome_dashboard.statistics", {
    start(){
        const statisticsdata = reactive({});

        async function loadStatistics(){
            const result =  await rpc("/awesome_dashboard/statistics",{});
            Object.assign(statisticsdata, result);
        } 

        loadStatistics();

        setInterval(loadStatistics,10000)
                return statisticsdata;
        }
});
