/** @odoo-module */

import { registry } from "@web/core/registry";


const myService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        setInterval(() => myfnc(rpc),10000);
        return {loadStatistics:() =>myfnc(rpc)}
    },
};

async function myfnc(rpc) {
    return rpc("/awesome_dashboard/statistics");
}


registry.category("services").add("awesome_dashboard.statistics", myService);