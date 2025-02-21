import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
  start() {
    const data = reactive({ isReady: false });
    const intervalId = setInterval(() => {
      loadStatistics();
    }, 10 * 60 * 5000);

    const loadStatistics = async () => {
      try {
        const statistics = await rpc("/awesome_dashboard/statistics");
        Object.assign(data, statistics, { isReady: true });
      } catch (error) {
        clearInterval(intervalId);
      }
    };

    loadStatistics();
    return data;
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
