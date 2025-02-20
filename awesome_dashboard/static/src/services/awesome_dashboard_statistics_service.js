import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";

const awesomeDashboardStatisticsService = {
  async: ["loadStatistics"],
  start() {
    return {
      loadStatistics: memoize(async () => {
        return await rpc("/awesome_dashboard/statistics");
      }),
    };
  },
};

registry.category("services").add("awesome_dashboard.statistics", awesomeDashboardStatisticsService);
