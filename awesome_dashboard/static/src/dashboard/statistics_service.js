import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

async function loadStatistics() {
    return rpc("/awesome_dashboard/statistics");
}

const cachedStatsServices = {
    start() {
        const statistics = reactive({ value: null });

        loadStatistics().then((value) => {
            statistics.value = value;
        });

        setInterval(
            () =>
                loadStatistics().then((value) => {
                    statistics.value = value;
                }),
            600_000
        );

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", cachedStatsServices);
