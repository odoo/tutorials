import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const dashboardService = {
    start() {
        const statistics = reactive({})
        // Sync localstorage with reactive state in DashboardDialog and Dashboard Component
        const state = JSON.parse(localStorage.getItem("awesome_dashboard.ItemsState")) || { removedIds: [] };
        const store = (obj) => localStorage.setItem("awesome_dashboard.ItemsState", JSON.stringify(obj));
        const itemsState = reactive(state, () => store(itemsState));
        store(itemsState);

        const loadStatistics = async () => {
            const updateStatistics = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updateStatistics);
        }
        setInterval(loadStatistics, 10 * 60 * 1000); // Calls after every 10 minutes
        loadStatistics();
        return { statistics, itemsState };
    }
}

registry.category("services").add("awesome_dashboard.statistics", dashboardService);
