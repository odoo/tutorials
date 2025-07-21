import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const statistics = reactive({ data: null, loading: true, error: null });

        async function fetchStatistics() {
            statistics.loading = true;
            statistics.error = null;
            try {
                const response = await rpc("/awesome_dashboard/statistics");
                statistics.data = response;
            } catch (e) {
                statistics.error = e;
            } finally {
                statistics.loading = false;
            }
        }

        async function fetchStatisticsRecursively() {
            await fetchStatistics();
            setTimeout(fetchStatisticsRecursively, 600000);
        }

        fetchStatisticsRecursively();

        return {
            statistics,
            reload: fetchStatistics
        };
    },
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
