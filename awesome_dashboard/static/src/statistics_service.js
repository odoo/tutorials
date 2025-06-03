/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const statisticsService = {
    start() {
        let data = null;
        return {
            loadStatistics: async () => {
                if (data) {
                    return data;
                }
                data = await rpc("/awesome_dashboard/statistics");
                return data;
            }
        };
    },
};

registry.category("services").add("load_statistics", statisticsService);
