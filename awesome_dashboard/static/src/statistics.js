import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        let reactivePayload = reactive({});
        let state = { timer: undefined};
        const service = {
            onUpdate: () => reactivePayload,
            loadStatistics: async () => {
                const result = await rpc("/awesome_dashboard/statistics");
                console.log(result);
                let data = {};
                for (const [key, value] of Object.entries(result)) {
                    data[key] = value;
                }
                reactivePayload = data;
                if(state.timer === undefined) {
                    // state.timer = setInterval(() => service.loadStatistics(), 600000); // 10 minutes
                    state.timer = setInterval(() => service.loadStatistics(), 10000); // 10 seconds
                }
                return data;
            },
        }
        
        return service;
    }
};

registry.category("services").add("statistics", statisticsService);