/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

class StatisticsService {
    constructor() {
        this.statistics = reactive({ data: null });

        this._loadStatistics = async () => {
            this.statistics.data = await rpc('/awesome_dashboard/statistics');
        };

        this._loadStatistics(); 

        setInterval(() => {
            this._loadStatistics();
        }, 10000); 
    }

    async loadStatistics() {
        return this.statistics.data;
    }
}

registry.category("services").add("awesome_dashboard.statistics", {
    start() {
        return new StatisticsService();
    },
});
