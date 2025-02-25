import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const TIMEOUT_SEC = 600;

const awesomeDashboardStatisticsService = {
  async start() {
    const statistics = reactive({ isReady: false });

    const loadStatistics = async () => {
      const updates = await rpc("/awesome_dashboard/statistics");
      Object.assign(statistics, { isReady: true, ...updates });
    };

    setInterval(loadStatistics, TIMEOUT_SEC * 1000); // setInterval expects milliseconds
    loadStatistics();

    return statistics;
  },
};

registry.category("services").add("awesome_dashboard.statistics", awesomeDashboardStatisticsService);
