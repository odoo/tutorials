import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export const statisticsService = {
    start () {
        const stats = reactive({
            data: {},
            isLoaded: false,
        })

        async function loadStatistics() {
            try {
                const updatedStats = await rpc("/awesome_dashboard/statistics");
                stats.data = updatedStats;
                stats.isLoaded = true;
            } catch(error) {
                console.log("An error occured: " + error);
            }
        }
        loadStatistics();
        setInterval(() => {
            loadStatistics();
        }, 10000);

        // console.log(loadStatistics);
        return {stats};
    }
};

registry.category("services").add("awesome_dashboard.statistics_service", statisticsService);
