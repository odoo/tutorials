/** @odoo-module **/

import { reactive } from "@odoo/owl"
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const INTERVAL_TIMEOUT = 600000;

async function loadStatistics() {
    try {
        return await rpc("/awesome_dashboard/statistics");
    } catch {
        return;
    }
}

export const myService = {
    dependencies: [],
    start(env, { }) {
        const statistics = reactive({ stats: null });
        loadStatistics().then((data) => statistics.stats = data).catch((err) => console.log(err))
        setInterval(async () => statistics.stats = await loadStatistics(), INTERVAL_TIMEOUT)
        return statistics;
    },
};

registry.category("services").add("loadStatistics", myService);
