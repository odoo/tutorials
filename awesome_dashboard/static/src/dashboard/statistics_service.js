/** @odoo-module **/
import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

export const statisticsService = {
  dependencies: ["rpc"],
  start(env, { rpc }) {
    let statistics = reactive({});

    async function retrieveStatistics() {
      let result = await rpc("/awesome_dashboard/statistics");
      Object.assign(statistics, result);
    }

    retrieveStatistics();
    setInterval(retrieveStatistics, 10 * 60 * 1000);

    return statistics;
  },
};

registry.category("services").add("statistics", statisticsService);
