import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const sharedStatistics = reactive({})

async function fetchStatistics(){
    try{
        const result = await rpc("/awesome_dashboard/statistics");
        for (const key in result) {
            sharedStatistics[key] = result[key];
        }
    }catch(e){
        console.error("Failed when trying to fetch", e);
    }
}

export const statisticsService = {
    start() {
        fetchStatistics();
        setInterval(fetchStatistics, 10*60*1000);
        return { 
            loadStatistics(){
                return sharedStatistics;
            }
        };
    },
};

registry.category("services").add("stats", statisticsService);
