/** @odoo-module */

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export const tshirtService = {
    dependencies: ["rpc"], // rpc is injected in the start function of the service by the service
    async: ["loadStatistics"], // loadStatistics is an async function
    start(env, { rpc }) { // rpc is injected in the start function of the service by the service
        return {
            loadStatistics: memoize(() => rpc("/awesome_tshirt/statistics")), // memoize is used to cache the result of the function so that it is not called again if the function is called with the same arguments
        };
    },
};

registry.category("services").add("tshirtService", tshirtService);
