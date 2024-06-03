/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({ data: {} });

        const fetchStatistics = async () => {
            statistics.data = await rpc("/awesome_dashboard/statistics");
        };

        setInterval(fetchStatistics, 10*60*1000);
        fetchStatistics().then();

        return statistics;
    }
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
