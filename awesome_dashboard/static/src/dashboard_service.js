import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";

const dashboardService = {
    start() {
        let stats = {}
        async function loadData() {
            stats = await rpc("/awesome_dashboard/statistics");
        }
        loadData();

        return { getStatistics: memoize(() => stats)}
    },
};


registry.category("services").add("awesome_dashboard.statistics", dashboardService);
