import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    start(env) {
        const stats = reactive({ data: {} });

        async function fetch() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats.data, result);
        }

        fetch();

        setInterval(fetch, 10000);

        return {
            statistics: stats.data,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
