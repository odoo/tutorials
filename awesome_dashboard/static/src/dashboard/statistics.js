/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { memoize } from "@web/core/utils/functions"; // Import memoize

const statisticsService = {
    start() {
        const statistics = reactive({ data: null, loading: true, error: null });

        async function _fetchStatistics() {
            statistics.loading = true;
            statistics.error = null;
            try {
                const response = await rpc("/awesome_dashboard/statistics");
                statistics.data = response;
                return response; 
            } catch (e) {
                statistics.error = e;
                throw e;
            } finally {
                statistics.loading = false;
            }
        }

        const loadStatistics = memoize(_fetchStatistics);
        loadStatistics(); 
        setInterval(_fetchStatistics, 600000); 


        return {
            statistics,
            loadStatistics,
        };
    },
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
