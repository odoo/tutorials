import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

const dashboardStatistics = {
    start(env) {
      const loadStatistics = memoize(async () => {
        return await rpc("/awesome_dashboard/statistics");
      });
      const state = reactive({ loadStatistics });
      setInterval(() => {
        const random = Math.random();
        state.loadStatistics = () => loadStatistics(random);
      }, 10 * 60 * 1000);
    
      return {
        state,
      };
    },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", dashboardStatistics);
