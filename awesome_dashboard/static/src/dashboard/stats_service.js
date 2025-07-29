/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

// export async function loadStatistics() {
//     return memoize(() => rpc("/awesome_dashboard/statistics"));
// }

const statsService = {
    start() {
        const stats = reactive({isReady: false});
        async function loadStatistics() {
            const new_vals = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, new_vals, {isReady: true});
        }

        setInterval(loadStatistics, 10*1000);
        loadStatistics();
        return stats;
    }
    
};


registry.category("services").add("awesome_dashboard.statistics", statsService);
