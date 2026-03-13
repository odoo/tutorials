import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        const state = reactive({
            data: null,
            isLoading: true,
        });
        async function load() {
            state.isLoading = true;

            const result = await rpc("/awesome_dashboard/statistics");

            state.data = result;
            state.isLoading = false;
        }

        load();

        setInterval(() => {
            load();
        }, 10000);

        return {
            state,
        };
    },
};

registry
    .category("services")
    .add("awesome_dashboard.statistics", statisticsService);
