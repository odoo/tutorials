import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const stats = reactive({});

export async function loadStatistics() {
    Object.assign(stats, await rpc("/awesome_dashboard/statistics"));
}

export const statisticService = {
    
    async start() {
        await(loadStatistics());

        setInterval(loadStatistics, 10000);

        return { stats };
    },
};