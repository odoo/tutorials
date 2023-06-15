/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export const myService = {
  dependencies: ["rpc"],
  async: ["loadstatistics"],
  start(env, { rpc }) {
    return {
      loadStatistics: memoize(function () {
        return rpc("/awesome_tshirt/statistics");
      // loadStatistics() {
      //   return memoize(rpc("/awesome_tshirt/statistics"));
      }),
    };
  },
};

registry.category("services").add("myService", myService);
