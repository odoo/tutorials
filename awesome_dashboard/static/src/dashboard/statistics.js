import {registry} from "@web/core/registry";
import {rpc} from "@web/core/network/rpc";
// import {memoize} from "@web/core/utils/functions";
import {reactive} from "@odoo/owl";

export const loadStatistics = {

    start: function () {
        const stats = reactive({isReady: false});

        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, updates, { isReady: true });
        }

        setInterval(loadData, 100000);
        loadData();

        return stats;
    }
}

registry.category("services").add("awesome_dashboard.statistics", loadStatistics);
