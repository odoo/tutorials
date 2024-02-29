/** @odoo-module **/
import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

export const statisticsService = {
    dependencies: ["rpc"],
    async start(env, { rpc }) {
        let stats = reactive({});

        async function loadStatistics() {
            let result = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, result);
        };

        await loadStatistics();

        setInterval(loadStatistics, 3000);

        return stats;
    }

};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
