import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const statisticsService = {
  start() {
    const stats = reactive({ isReady: false });

    async function updateStats() {
      const newStats = await rpc("/awesome_dashboard/statistics");
      Object.assign(stats, newStats, { isReady: true });
    }

    setInterval(updateStats, 10 * 60 * 1000);
    updateStats();

    return stats
  },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
