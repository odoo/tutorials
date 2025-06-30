import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export const loadStatistics = {
    start() {
        const data = reactive({ isReady: false })

        async function loadData() {
            const update = await rpc("/awesome_dashboard/statistics");
            Object.assign(data, update, { isReady: true })
        }

        setInterval(loadData, 10*60*1000);
        loadData();

        return data
    },
};

registry.category("services").add("awesome_dashboard.statistics", loadStatistics);