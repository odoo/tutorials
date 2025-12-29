import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statistics = {
    dependencies: [],
    start(env) {
        
        const ret = reactive({isReady:false})
        async function loadStatistics()
        {
            Object.assign(ret, await rpc("/awesome_dashboard/statistics"), {isReady:true});
        }
        setInterval(loadStatistics,1000*60*10);
        
        loadStatistics();
        return ret;
        }
    };
    registry.category("services").add("awesome_dashboard.statistics",statistics)
