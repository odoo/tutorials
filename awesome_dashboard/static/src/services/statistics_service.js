import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

const statisticsData = reactive({});

async function reloadStatistics() {
    try {
        const result = await rpc("/awesome_dashboard/statistics", {});
        Object.assign(statisticsData, result);
        console.log("stat", statisticsData)

    } catch (error) {
        console.error("Error reloading statistics:", error);
    }
}

setInterval(reloadStatistics, 10000);

export const statisticsService = {
    dependencies: [],
    start() {
        reloadStatistics();
        return {
            data: statisticsData,
            reload: reloadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
