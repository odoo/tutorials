import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    async: ["loadStatistics"],
    start() {
        const loadStatistics = () => rpc("/awesome_dashboard/statistics")
        const state = reactive({ data: null });
        const fetchData = async () => {
            state.data = await loadStatistics();
        };
        fetchData();
        setInterval(fetchData, 10000);
        return {
            state: state
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
