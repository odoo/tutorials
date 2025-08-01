/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";






export const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });

        async function reloadStatistics() {
            try {
                const newData = await rpc("/awesome_dashboard/statistics");

            
                
               Object.assign(statistics, newData, { isReady: true });

            } catch (e) {
                console.error("Failed to reload statistics:", e);
            }
        }


       
        reloadStatistics();
        setInterval(reloadStatistics, 10 * 1000);
        
        return statistics;
    }
        

};


registry.category("services").add("aleksaStatistics", statisticsService);


/****


import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

// Memoized function defined ONCE
const loadStatistics = reactive(memoize(async () => {
    return await rpc("/awesome_dashboard/statistics");
}));

export const statisticsService = {
    start() {
        return {
            loadStatistics,
        };
    },
   
};

registry.category("services").add("aleksaStatistics", statisticsService);
*/
