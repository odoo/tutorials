import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

export const statisticsService = {
    start() {
        const state = reactive({ data: {} });
        async function getData() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(state, data);
        }
        getData();
        setInterval(getData, 600000);
        return state;
    }
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
