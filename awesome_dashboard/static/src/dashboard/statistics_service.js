/** @odoo-module **/

import {registry} from "@web/core/registry";
import {reactive} from "@odoo/owl";


export async function loadStatistics(rpc) {
    return rpc("/awesome_dashboard/statistics");
}

export const statisticsService = {
    dependencies: ["rpc"],
    start(env, {rpc}) {
        const statistics = reactive({});

        async function loadData() {
            const updates = await loadStatistics(rpc);
            Object.assign(statistics, updates);
        }


        loadData().then(() => {
            setInterval(loadData, 10 * 60 * 1000);
        });


        return statistics;
    }
}


registry.category("services").add("statistics_service", statisticsService);