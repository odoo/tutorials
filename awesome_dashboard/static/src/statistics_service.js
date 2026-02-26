import { browser } from "@web/core/browser/browser";
import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export const statisticsService = {
    start(env) {
        let stats = reactive({});

        async function _loadStats() {
            try {
                const data = await rpc("/awesome_dashboard/statistics");
                Object.assign(stats, data);
            } catch (e) {
                console.error("Failed to load stats", e);
            }
        }

        _loadStats();

        browser.setInterval(() => {
            _loadStats();
            console.log("Stats updated: ", stats);
        }, 100000);

        return stats;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
