import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        const stats = reactive({ isReady: false });

        async function loadData() {
            const res = memoize(() => rpc("/awesome_dashboard/statistics"));
            Object.assign(stats, res, { isReady: true });
        }

        setInterval(loadData, 600);
        loadData();

        return stats;
    },
};

registry
    .category("services")
    .add("awesome_dashboard.statistics", statisticsService);
