/** @odoo-module **/

import { reactive } from "@odoo/owl"
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions"

export const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {

        const statistics = reactive({values: {}});

        const loadStatistics = async () => {
            statistics.values = await rpc("/awesome_dashboard/statistics")
        }

        loadStatistics()
        setInterval(async function () {
            loadStatistics()
        }, 5000);
        
        // MEMOIZED
        // const loadStatistics = memoize(
        //     async function loadStatistics() {
        //         const result = await rpc("/awesome_dashboard/statistics");
        //         return result;
        //     }
        // );

        return { statistics };
    },
};

registry.category("services").add("statistics", statisticsService);