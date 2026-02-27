import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statistics = {
    async start() {
        const data = reactive({loadStatistics: memoize(() => rpc("/awesome_dashboard/statistics"))})

        setInterval(async () => {
            data.loadStatistics = memoize(() => rpc("/awesome_dashboard/statistics"));
        }, 1_000*10)

        return {
            data: data
        }
    }
}

registry.category("services").add("statistics", statistics)