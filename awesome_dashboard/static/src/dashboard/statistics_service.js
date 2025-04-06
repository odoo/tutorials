import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

// Service to fetch and manage dashboard statistics
const statisticsService = {
    start() {
        // Reactive state for statistics, initially not ready
        const statistics = reactive({ isReady: false });

        // Function to load statistics data from the backend
        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            // Updating the reactive state with fetched data and marking it ready
            Object.assign(statistics, updates, { isReady: true });
        }

        // Periodically refresh data every 10 minutes
        setInterval(loadData, 10 * 60 * 1000);
        
        // Initial data load
        loadData();

        // Returning the reactive statistics state
        return statistics;
    },
};

// Registering the statistics service in the service registry
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
