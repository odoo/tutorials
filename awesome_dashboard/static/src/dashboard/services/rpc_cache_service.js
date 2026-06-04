import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export const statisticsService = {
    start() {
        const statistics = reactive({});

        async function reload() {

            try {
                const result = await rpc("/awesome_dashboard/statistics");
                Object.assign(statistics, result);
            }
            catch (error) {
                console.error("Failed to load statistics:", error);
            }
        }

        reload();
        setInterval(reload, 50 * 1000);

        return { statistics };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);