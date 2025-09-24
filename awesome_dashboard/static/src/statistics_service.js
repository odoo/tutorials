import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const fetchStatistics = () => {
    return rpc("/awesome_dashboard/statistics");
}

export const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });
        const updateData = async () => {
            Object.assign(statistics, await fetchStatistics(), { isReady: true });
        }
        updateData();
        setInterval(updateData, 1000 * 60 * 10);
        return statistics;
    },
}

registry.category("services").add("statistics_service", statisticsService);