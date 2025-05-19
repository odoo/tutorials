import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


export const statisticsService = {
    async start() {
        const state = reactive({isDone: false})
        const intervalId = setInterval(loadStatistics, 10 * 1000 * 60)

        async function loadStatistics() {
            try {
                const result = await rpc("/awesome_dashboard/statistics");
                Object.assign(state, result, {isDone: true});
            } catch (error) {
                Object.assign(state, {isDone: false});
                clearInterval(intervalId);
                console.error("Error fetching statistics:", error);
            }
        }

        await loadStatistics();

        return state;
    },
};


registry.category("services").add("awesome_dashboard.statistics", statisticsService);
