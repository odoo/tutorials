import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";


export const statisticsService = {
    async: ['loadStatistics'],
    start() {
        /*return {
            loadStatistics: memoize(() => rpc("/awesome_dashboard/statistics")),
        }*/
        let data = { orders_by_size: {} };
        const callRpc = async function(){
            data = await memoize(() => rpc("/awesome_dashboard/statistics"))();
            console.log(data);
        }
        callRpc();
        setInterval(callRpc, 5000);

        return reactive({
            loadStatistics: (() => data),
        })
    }
};

registry.category("services").add("statistics", statisticsService);
