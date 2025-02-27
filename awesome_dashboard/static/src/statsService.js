import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const statsService = {
    async: ["loadStats"],
    start() {
        return { loadStats: memoize(() => rpc("/awesome_dashboard/statistics")) }; 
    }
};

registry.category("services").add("awesome_dashboard.statistics",statsService);
