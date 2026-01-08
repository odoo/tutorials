import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";


const statisticsService = {
    start() {
        const stats = reactive({ isReady: false });

        async function loadData() {
            const fetchedStats = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, fetchedStats, { isReady: true });
        }

        loadData();

        setInterval(async () => {
            loadData();
        }, 1000*10);

        return stats
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);