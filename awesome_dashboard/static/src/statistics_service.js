import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

const statisticsService = {
    async: ["preload"],
    start() {
        return {
            loadStatistics: memoize((url) => rpc(url)),
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
