import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

async function loadData() {
    return await rpc("/awesome_dashboard/statistics");
}

export const StatisticsService = {
    interval: null,
    async start() {
        const reactiveStatistics = reactive({ isReady: false }, () => {
            console.log("StatisticsService: reactive data object has been updated.");
        });

        const fetchDataAndUpdate = async () => {
            try {
                const newData = await loadData();     // remove memoized cache
                Object.assign(reactiveStatistics, newData, { isReady: true });
            } catch (e) {
                console.error("Failed to fetch data:", e);
            }
        };
        await fetchDataAndUpdate();
        this.interval = setInterval(fetchDataAndUpdate, 10000 * 60 * 10); // every 10 minutes
        return reactiveStatistics;

    },
    onDestroy() { // used with Services to clean up when the service is stopped
        clearInterval(this.interval);
    }
};
registry.category("services").add("awesome_dashboard.statistics", StatisticsService);
