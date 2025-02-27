import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
  start() {
    return {
      loadStatistics: memoize(async () => {
        try {
          return await rpc("/awesome_dashboard/statistics");
        } catch (error) {
          console.error("loadStatistics failed:", error);
          throw new Error("Failed to load statistics");
        }
      }),
    };
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
