import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });

        async function loadData() {
            Object.assign(statistics, { isReady: false });
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        }

        setInterval(loadData, 10000);
        loadData();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.Statistics", statisticsService);
