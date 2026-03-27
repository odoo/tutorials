import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {

        const state = reactive({data: {}});

        const loadStatistics = (async () => {
            
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(state.data, result);
        });
        
        loadStatistics();

        // setInterval(loadStatistics, 3000);

        return {
            state,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
