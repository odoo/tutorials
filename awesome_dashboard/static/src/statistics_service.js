/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl"

export async function loadStatistics() {
    return await rpc("/awesome_dashboard/statistics");
}

export const statisticsService = {

    start() {
        const statistics = reactive({ isReady: false });
        setInterval(async () => {
            statistics.stats = await loadStatistics();
        }, 10 * 1000);
        loadStatistics().then((stats) => {
            statistics.stats = stats;
            statistics.isReady = true;
        })
        return statistics;
    },
};

registry.category("services").add("statistics", statisticsService);
