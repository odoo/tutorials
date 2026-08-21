import { reactive } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    async _loadData(statistics) {
        const updates = await rpc("/awesome_dashboard/statistics");
        Object.assign(statistics, updates, { isReady: true });
    },

    start() {
        const statistics = reactive({ isReady: false });

        setInterval(() => this._loadData(statistics), 10_000);
        this._loadData(statistics);

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
