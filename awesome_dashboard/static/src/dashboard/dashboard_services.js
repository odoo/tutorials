
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl"


registry.category("services").add("awesome_dashboard.statistics", {
    start() {
        let stats = reactive({});

        async function loadStatistics() {
            let res = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, res);
        }

        loadStatistics();
        setInterval(loadStatistics, 10 * 1000);

        return stats;
    }
});
