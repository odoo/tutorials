/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

async function fetchStatistics() {
  return await rpc("/awesome_dashboard/statistics", {});
}

export const statisticsService = {
  dependencies: [],
  start() {
    const stats = reactive({});

    async function loadAndUpdateStatistics() {
      const newStats = await fetchStatistics();
      Object.assign(stats, newStats);
    }
    loadAndUpdateStatistics();

    setInterval(() => {
      loadAndUpdateStatistics();
    }, 10000);

    return {
      getStatistics: () => stats,
    };
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
