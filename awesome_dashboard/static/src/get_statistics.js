import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

export const getStatistics = {
    async start() {
        return {
            loadStatistics: memoize(() => rpc("/awesome_dashboard/statistics")),
        };    
    },
};

registry.category("services").add("awesome_dashboard.getStats", getStatistics);
