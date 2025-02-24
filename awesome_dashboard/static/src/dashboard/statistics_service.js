/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { browser } from "@web/core/browser/browser";

export const statisticsService = {
    start() {
        const stats = reactive({});
        browser.setInterval(async () => {
            stats.result = await rpc("/awesome_dashboard/statistics");
        }, 10 * 60 * 1000);
        return {
            getStatsResult: () => {
                if (!stats.results) {
                    rpc("/awesome_dashboard/statistics").then((value) => {
                        stats.result = value;
                    });
                }
                return stats;
            }
        };
    }
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
