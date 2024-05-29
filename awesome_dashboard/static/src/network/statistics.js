/** @odoo-module */

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";


const myService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        return {loadStatistics:myfnc(rpc)};
    },
};

function myfnc(rpc) {
    return memoize(() => rpc("/awesome_dashboard/statistics"));
}


registry.category("services").add("awesome_dashboard.statistics", myService);