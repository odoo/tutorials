import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

async function loadStatistics(statistics) {
  const updates = await rpc("/awesome_dashboard/statistics");
  Object.assign(statistics, updates, { isReady: true });
}

const statisticsService = {
  start() {
    const statistics = reactive({ isReady: false });

    setInterval(loadStatistics(statistics), 600 * 1000);

    loadStatistics(statistics);

    return statistics;
  },
};

registry.category("services").add("statistics", statisticsService);
