import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });

        async function update() {
            const value = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, value, { isReady: true });
        }

        setInterval(update, 10*60*1000);
        update()

        return statistics
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
