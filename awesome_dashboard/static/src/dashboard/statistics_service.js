/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

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

setInterval(fetchStatistics, 5000);

registry.category("services").add("awesome_dashboard.statistics", {
    start() {
        return { statistics };
    },
});
