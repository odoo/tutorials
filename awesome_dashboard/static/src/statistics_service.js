import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from '@odoo/owl';

export const statisticsService = {
    start(env) {
        const loadStatistics = memoize(() => rpc("/awesome_dashboard/statistics"));
        
        const statistics = reactive({})


        async function update(){
            const data = await rpc("/awesome_dashboard/statistics")
            Object.assign(statistics, data);
            console.log(statistics)
        }
        
        update();
        
        const interval = setInterval(update, 5000);
        
        
        return {
            statistics
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);