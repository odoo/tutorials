import { reactive, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

export async function loadStatistics() {
    return await rpc("/awesome_dashboard/statistics");
}

export const statisticsService = {
    async start() {
        const state = reactive({ value: await loadStatistics() }); 

        setInterval(async () => {
            state.value = await loadStatistics(); 
        }, 10*60*1000);

        return state;
    }
}

registry.category("services").add("statistics", statisticsService);
