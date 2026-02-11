import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


export const statisticsService = {
  start(env) {
        const statistics = reactive({
              isReady: false,
        });

     async function loadData() {
          const newData = await rpc("/awesome_dashboard/statistics");
          Object.assign(statistics, newData, { isReady: true });
     }
     loadData();
     setInterval(loadData,10000);

     return statistics;

  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
