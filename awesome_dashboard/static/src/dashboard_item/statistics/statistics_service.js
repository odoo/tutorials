/** @odoo-module **/
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export const statisticsService = {
  dependencies: ["rpc"],
  start(env, { rpc }) {
    return memoize(() => rpc("/awesome_dashboard/statistics"));
  },
};

registry.category("services").add("statistics", statisticsService);
