import {registry} from "@web/core/registry";
import {rpc} from "@web/core/network/rpc";
// import {memoize} from "@web/core/utils/functions";
import { reactive } from "@odoo/owl"; 

const statistics = reactive({ isReady: false});
const fetchData = async () => {
    try {
        const result = await rpc("/awesome_dashboard/statistics");
        console.log(result)
        Object.assign(statistics, result, {isReady: true});
    } catch (error) {
        console.log(error)
    }
}
setInterval(fetchData, 1000);
const statisticsService = {
        start() {         
            fetchData();
            return statistics;
        }
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService)
