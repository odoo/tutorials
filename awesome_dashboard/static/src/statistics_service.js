import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export async function loadStatistic() {
    return await rpc("/awesome_dashboard/statistics");
}

export const statisticsService = {
    async start() {
        const data = reactive(await loadStatistic());

        setInterval(async () => {
            data = await loadStatistic();
        }, 10 * 60 * 1000);

        return data;
    }
}

registry.category("services").add("statistics", statisticsService);
