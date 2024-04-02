/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl"
import { useService } from "@web/core/utils/hooks";

export const Statistics = {
    
    start() {
        const statistics = reactive({ isReady: false });
        this.rpc = useService("rpc")

        async function loadData() {
            const updates = await this.rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        }

        setInterval(loadData, 600000);
        loadData();

        return statistics;
    }
};

registry.category("services").add("awesome_dashboard.statistics", Statistics);
