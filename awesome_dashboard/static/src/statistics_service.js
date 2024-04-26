/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

const statistics = {
    dependencies: ['rpc'],
    start(env, { rpc }) {
        let stats = reactive({});

        async function loadStatistics() {
            Object.assign(stats, await rpc('/awesome_dashboard/statistics'))
        }

        setInterval(loadStatistics, 10000);
        loadStatistics();

        return stats;
    }
}

registry.category("services").add("statistics", statistics)

