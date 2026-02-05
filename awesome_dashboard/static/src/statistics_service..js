import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";

export const statisticsService = {
  async: ["loadStatistics"],
  start(env) {
    return {
      loadStatistics: memoize(() => {
        return rpc("/awesome_dashboard/statistics");
      }),
    };
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
