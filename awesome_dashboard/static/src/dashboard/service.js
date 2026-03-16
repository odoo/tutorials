import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticService = {
    start() {
        const statistics = reactive({ isReady: false });

        async function loadData() {
            const stat = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, stat, { isReady: true });
        }

        setInterval(loadData, 25 * 1000);
        loadData()

        return statistics
    },
}

registry.category("services").add("awesome_dashboard.statistic_service", statisticService);
