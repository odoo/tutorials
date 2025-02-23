/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";


export const statisticsService = {

  start() {
    const statistics = reactive({ isLoading: false });

    const loadStatistics = async () => {
      statistics.isLoading = true;
      try {
        const updated_value = await rpc("/awesome_dashboard/statistics");
        Object.assign(statistics, updated_value, {isLoading: false});
      } catch (error) {
        console.error("Failed to load statistics:", error);
        statistics.isLoading = false;
      }
    };

    // Initial Load
    loadStatistics();

    // Auto-refresh every 10 seconds
    setInterval(loadStatistics, 100000);


    return statistics;
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
