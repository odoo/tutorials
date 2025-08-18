import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


const statisticsService = {
    start() {
        const statistics = reactive({ ready: false })
        
        async function updateStatistics() {
            const updated = await rpc("/awesome_dashboard/statistics")
            Object.assign(statistics, updated, {ready : true})
        }
        setInterval(updateStatistics, 10000)
        // updateStatistics()

        return statistics
    },

};


registry.category("services").add("awesome_dashboard.statistics", statisticsService);