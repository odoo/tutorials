import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

export async function loadStatistics() {
  return await rpc("/awesome_dashboard/statistics");
}

export const statisticsService = {
  start() {
    const state = reactive({});

    async function loadAndUpdateStats() {
      Object.assign(state, await loadStatistics());
    }

    loadAndUpdateStats();

    setInterval(loadAndUpdateStats, 10 * 1000);
    return state;
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
