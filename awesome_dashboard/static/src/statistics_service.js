import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

export async function loadStatistics() {
    return await rpc('/awesome_dashboard/statistics');
}

export const statisticsService = {
    async start() {
        const statisticsBox = reactive({statistics: await loadStatistics()});
        setInterval(async () => {
            statisticsBox.statistics = await loadStatistics();
        }, 10 * 60 * 1000);
        return statisticsBox;
    },
    
}

registry.category("services").add("statistics", statisticsService);
