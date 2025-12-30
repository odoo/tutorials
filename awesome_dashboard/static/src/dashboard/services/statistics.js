import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsState = reactive({
    loading: true,
    data: {},
});
async function fetchStatistics() {
    const result = await rpc("/awesome_dashboard/statistics");
    statisticsState.data = result;
    statisticsState.loading = false;
}

export const statisticsService = {
    start() {
        fetchStatistics();
        setInterval(fetchStatistics, 10000);
        return {
            statistics: statisticsState,
            reload: fetchStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
