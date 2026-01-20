import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetch() {
    sleep(1000);
    return await rpc("/awesome_dashboard/statistics");
}

const dashboardStatsService = {
    async: ["fetchNow"],


    start(env, {}) {
        const data_proxy = reactive({data: {}});

        // Better to not use memoize since the cache needs to be invalidated.
        // memoized_fetch = memoize(fetch); 

        setInterval(async ()=>{
            data_proxy.data = await fetch();
        }, 10000);

        const getDataProxy = ()=>{
            return data_proxy;
        }
        
        const fetchNow = ()=>{
            return fetch();
        }

        return { getDataProxy, fetchNow };
    },
};

registry.category("services").add("awesome_dashboard.dashboard_stats", dashboardStatsService);