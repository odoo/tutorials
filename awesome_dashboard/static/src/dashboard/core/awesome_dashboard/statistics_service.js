import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";


const statisticsService = {
  start() {
    const stats = reactive({});

    async function loadStats() {
      const stats_data = await rpc("/awesome_dashboard/statistics");
      Object.assign(stats, stats_data);
    }

    loadStats();
    setInterval(loadStats, 10000*60);

    return stats;
  },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
