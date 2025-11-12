/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const statistics = reactive({ data: null });

async function fetchStatistics() {
    try {
        const result = await rpc("/awesome_dashboard/statistics", {});
        Object.assign(statistics, { data: result });
    } catch (error) {
        console.error("Error fetching statistics:", error);
    }
}

fetchStatistics();

setInterval(fetchStatistics, 1000);

registry.category("services").add("awesome_dashboard.statistics", {
    start() {
        return { statistics };
    },
});
