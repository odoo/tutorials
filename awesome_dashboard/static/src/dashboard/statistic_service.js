/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

const statistics = {
    dependencies: ["rpc"],
    start(env, { rpc }){

        const stats = reactive({isReady: false});

        async function loadStatistics() {
            let res = await rpc("/awesome_dashboard/statistics");

            Object.assign(stats, res, {isReady: true});
            console.log(stats);
         }


        setInterval(async () => {
            await loadStatistics();
        }, 1000*60*10);

        loadStatistics();

//        loadStatistics().then(() => {
//            setInterval(loadStatistics, 10);
//        });

        return stats
    }
}

registry.category("services").add("awesome_dashboard.statistics", statistics);
