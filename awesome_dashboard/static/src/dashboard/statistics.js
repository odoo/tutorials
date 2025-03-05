import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
  start() {
    const stats = reactive({ });

    const intervalId = setInterval(() => {
      loadStatistics();
    }, 2 * 1000);

    const loadStatistics = async () => {
      try {
        const statistics = await rpc("/awesome_dashboard/statistics");
        Object.assign(stats, statistics);
      } catch (error) {
        clearInterval(intervalId);
        console.error("Error fetching statistics:", error);
      }
    };

    loadStatistics();

    return stats;
  },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
