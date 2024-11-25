/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const serviceStatistics = {
    start(){
        const statistics = reactive({ });
        async function statisticsLoad() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, result);
        }
        setInterval(statisticsLoad, 10000); /** Timout set to 10 seconds for testing **/
        statisticsLoad();
        return statistics;
    }
}

registry.category("services").add("awesome_dashboard.statistics", serviceStatistics);