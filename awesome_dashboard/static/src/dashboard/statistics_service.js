/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

const statistics = {
    dependencies: ['rpc'],
    start(env, { rpc }) {
        let stats = reactive({ isReady: false });

        async function loadStatistics() {
            const data = await rpc('/awesome_dashboard/statistics')
            Object.assign(stats, data, { isReady: true })
        }

        setInterval(loadStatistics, 10000);
        loadStatistics();

        return stats;
    }
}

registry.category("services").add("statistics", statistics)

