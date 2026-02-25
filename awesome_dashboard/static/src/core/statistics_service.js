import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statistics = {
    async start() {
        const data = reactive({statistics: await rpc("/awesome_dashboard/statistics")})

        setInterval(async () => {
            const getStatistics = await rpc("/awesome_dashboard/statistics");
            data.statistics = getStatistics;
            console.log(data)
        }, 1_000*10)

        return {
            data: data
        }
    }
}

registry.category("services").add("statistics", statistics)