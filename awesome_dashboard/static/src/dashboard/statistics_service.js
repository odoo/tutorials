/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";


const statisticsService = {
    start() {
        const data = reactive({});
        const loadStatistics = async () => {
            try {
                const result = await rpc("/awesome_dashboard/statistics");
                Object.keys(data).forEach(key => delete data[key]);
                Object.assign(data, result);

            } catch (error) {
                console.error('Error loading statistics:', error);
            }
        };
        loadStatistics();

        setInterval(loadStatistics, 50000);

        return {
            data,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
