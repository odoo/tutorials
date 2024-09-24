/** @odoo-module */

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

const statisticsService = {
    dependencies: ["rpc"],
    start(env, {rpc}) {
        const statistics = reactive({
            dataAvailable: false,
            refreshing: false,
            lastUpdate: null,
        })

        async function refresh() {
            statistics.refreshing = true;
            Object.assign(statistics, await rpc("/awesome_dashboard/statistics"), {
                dataAvailable: true,
                refreshing: false,
                lastUpdate: new Date(),
            });
        }

        setInterval(refresh, 5000);

        return {
            statistics,
            refresh,
        }
    }
}
registry.category("services").add("awesome_dashboard.statistics", statisticsService);