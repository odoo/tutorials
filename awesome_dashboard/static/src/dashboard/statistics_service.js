import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statistics = reactive({});

async function loadStatistics() {
  const result = await rpc("/awesome_dashboard/statistics");
  if (result) {
    Object.assign(statistics, result);
  }
}

loadStatistics();
setInterval(loadStatistics, 1000);

registry.category("services").add("awesome_dashboard.statistics", {
  start() {
    return statistics;
  },
});
