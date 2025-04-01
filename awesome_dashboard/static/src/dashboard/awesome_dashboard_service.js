import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

export const statisticsService = {
  dependencies: [],
  start() {
    const data = reactive({});
    async function loadStatistics() {
      const result = await rpc("/awesome_dashboard/statistics", {});
      Object.assign(data, result);
    }

    loadStatistics();

    setInterval(loadStatistics, 10000);
    return {
      data,
      loadStatistics,
    };
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
