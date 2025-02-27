import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
  start() {
    const statistics = reactive({ flag: false });

    async function loadStatistics() {
      try {
        const result = await rpc("/awesome_dashboard/statistics");
        Object.assign(statistics, result, { flag: true });
      } catch (error) {
        console.error("loadStatistics failed:", error);
      }
    }

    loadStatistics();
    setInterval(loadStatistics, 10000);

    return statistics;
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
