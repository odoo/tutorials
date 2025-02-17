import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
  start() {
    //for memoizing the function calls
    // return {
    //    loadStatistics: memoize(()=> rpc("/awesome_dashboard/statistics")),
    // };

    const statistics = reactive({ isReady: false });

    async function loadData() {
      const updates = await rpc("/awesome_dashboard/statistics");
      Object.assign(statistics, updates, { isReady: true });
    }

    setInterval(loadData, 10 * 60 * 1000);
    loadData();

    return statistics;
  },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService)
