/** @odoo-module */

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

const statisticsService = {
  dependencies: ["rpc"],
  async: ["loadStatistics"],
  start(_, { rpc }) {
    return {
      load: memoize(() => rpc("/awesome_dashboard/statistics")),
    };
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
