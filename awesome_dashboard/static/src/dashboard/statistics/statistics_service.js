import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        const statistics = reactive({ value: {} });

        async function fetchAndUpdate() {
            const newData = await rpc("/awesome_dashboard/statistics");
            statistics.value = newData;
        }

        fetchAndUpdate();
        setInterval(fetchAndUpdate, 600000);

        return { statistics, reload: fetchAndUpdate };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
