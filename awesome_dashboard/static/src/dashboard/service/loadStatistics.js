import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import {reactive } from "@odoo/owl";


console.log('statics service loaded....');

export const loadStatistics = async ()=> {
    return await rpc('/awesome_dashboard/statistics') //rpc(route, params, settings)
}

export const loadStatisticsService = {
    
    async start () {
        const INTERVAL = 10*1000;
        const state= reactive({staticData: {}})

        Object.assign(state.staticData, await loadStatistics())

        setInterval(async() => {
            Object.assign(state.staticData, await loadStatistics())
        }, INTERVAL);

        return state
    }
}

registry.category("services").add("awesome_dashboard.statistics", loadStatisticsService)
