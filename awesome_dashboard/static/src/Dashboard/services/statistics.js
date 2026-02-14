import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


export const statistics = {
    start() {
        const statistics = reactive({
            isReady: false,
        });
        const callrpc = async () => {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, result, { isReady: true });
        };
        callrpc();
        setInterval(callrpc, 10000);
        return statistics;
    }
}

registry.category("services").add("statistics", statistics);
