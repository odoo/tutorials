import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc"
const statisticsService = {
  dependencies: [],
  start() {
    const statistic = reactive({ data: null, loading: true, error: null });

    async function fetchData() {
      statistic.loading = true;
      statistic.error = null;
      try {
        statistic.data = await rpc("/awesome_dashboard/statistics");
      } catch (error) {
        statistic.error;
      } finally {
        statistic.loading = false;
      }
    }

    fetchData();

    setInterval(fetchData, 5000);
    return { statistic };
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
