import { rpc } from "@web/core/network/rpc"
import { registry } from "@web/core/registry"
import { reactive } from "@odoo/owl"

const REFRESH_TIME = 600000

export const statistics = {
    depedencies: [],
    async start(env){
        const data = reactive({ stat: {} });

        async function loadStat(){
            const newstat =  await rpc("/awesome_dashboard/statistics");
            Object.assign(data.stat, newstat)
        }
        loadStat()
        setInterval(loadStat,REFRESH_TIME)
        return { data };

    }
};

registry.category("services").add("awesome_dashboard.statistics",statistics)
