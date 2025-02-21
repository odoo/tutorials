import {registry} from "@web/core/registry";
import {memoize} from "@web/core/utils/functions";
import {rpc} from "@web/core/network/rpc";

const loadStatistics= memoize(async()=>{
    const data= await rpc("/awesome_dashboard/statistics", {});
    return data;
})

const AwesomeDashboardStatisticsService={
    start() {
        return {
            loadStatistics,
        };
    }
}
registry.category('services').add('awesome_dashboard.statistics', AwesomeDashboardStatisticsService)
