import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";

const refreshIntervalSec = 10;

// Methods of retrieving data. State returned in consistent way across all methods 
const loader = {
    loadStatistics: async () => {
        let state = {}
        state.data = await memoize(() => rpc("/awesome_dashboard/statistics"))();
        return state;
    },
    loadStatisticsRPC: async () => { 
        let state = {}
        state.data = await rpc("/awesome_dashboard/statistics");
        return state;
    },
};

const statisticStateService = {
    async start(env) {

        const state = reactive({ data: (await loader.loadStatisticsRPC()).data});
        setInterval(async () => state.data = (await loader.loadStatisticsRPC()).data, refreshIntervalSec * 1000)

        return {
            ...loader,
            loadStatisticsRealTime: () => state,
        }
    },
};

registry.category("services").add("statistics_service", statisticStateService);