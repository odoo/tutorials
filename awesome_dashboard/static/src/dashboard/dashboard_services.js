
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";


registry.category("services").add("awesome_dashboard.statistics", {
    async: ["loadStatistics"],
    start() {
        async function loadStatistics() {
            return await rpc("/awesome_dashboard/statistics");
        }
        return {
            loadStatistics: memoize(loadStatistics),
        }
    }
});
