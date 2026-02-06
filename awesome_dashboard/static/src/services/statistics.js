import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

export const statistics = {
    start() {
        const callrpc = memoize(async () => {
            const result = await rpc("/awesome_dashboard/statistics");
            return result;
        });
        return { callrpc };
    }
}

registry.category("services").add("statistics", statistics);