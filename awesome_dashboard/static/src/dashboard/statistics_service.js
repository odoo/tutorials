/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const stats = reactive({ data: null });

        const load = async () => {
            const result = await rpc("/awesome_dashboard/statistics", {});
            stats.data = result; // update in place
        };

        load();                 // first load (async)
        setInterval(load, 10000); // refresh every 10s

        return stats;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
