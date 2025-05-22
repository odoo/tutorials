import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

/**
 * Service to fetch and manage dashboard statistics
 * 
 * This service fetches dashboard data from the server and
 * provides it to dashboard components. Data is automatically
 * refreshed at regular intervals.
 */
const statisticsService = {
    /**
     * Initialize the statistics service
     * @returns {Object} Reactive statistics object
     */
    start() {
        // Create a reactive statistics object
        const statistics = reactive({ isReady: false });

        /**
         * Fetch fresh data from server
         * @returns {Promise} Promise that resolves when data is loaded
         */
        async function fetchStatistics() {
            try {
                const data = await rpc("/awesome_dashboard/statistics");
                // Update statistics with fetched data
                Object.assign(statistics, data, { isReady: true });
            } catch (error) {
                console.error("Failed to fetch dashboard statistics:", error);
            }
        }

        // Refresh data every 10 minutes
        const REFRESH_INTERVAL = 10 * 60 * 1000; // 10 minutes
        const intervalId = setInterval(fetchStatistics, REFRESH_INTERVAL);
        
        // Load data immediately
        fetchStatistics();
        
        // Return the reactive statistics object
        return statistics;
    },
};

// Register the service
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
