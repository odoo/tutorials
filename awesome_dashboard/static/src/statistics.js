import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

export let loadStatistics = memoize(() => rpc("/awesome_dashboard/statistics"));

export const statistics = {
    start() {
        return { loadStatistics };
    }
};

registry.category("services").add("awesome_dashboard.statistics", statistics);
