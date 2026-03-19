import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const StatService = {
    start() {
        const state = reactive({
            data: null,
        });
        function sleep(ms) {
            return new Promise((resolve) => setTimeout(resolve, ms));
        }

        async function loadStats() {
            await sleep(5000)
            const result = await rpc("/awesome_dashboard/statistics");
            state.data = result;
        }

        loadStats();

        setInterval(loadStats, 5000);

        return {
            state,
        };
    },
};

registry.category("services").add("statistics", StatService);
