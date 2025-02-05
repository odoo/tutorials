/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


const REFRESH_TIME = 5000;

export const statisticsService = {
    async start() {
        const state = reactive({
            values: {}
        })

        async function loadStatistics(){
            const res = await rpc("/awesome_dashboard/statistics", {});
            Object.assign(state.values, res)
            // console.log(state)
        }
        
        await loadStatistics();
        setInterval(loadStatistics, REFRESH_TIME)

        return{
            state
        }
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
