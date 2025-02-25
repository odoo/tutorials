import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl"

const data = reactive({});

const loadStatistics = async () => {
    const newData = await rpc("/awesome_dashboard/statistics", {});
    Object.assign(data, newData);
    console.log(data)
    return data;
}
loadStatistics();
setInterval(() => loadStatistics(), 10 * 60 * 1000);

const AwesomeDashboardStatisticsService = {
    start() {
        return {
            data,
            loadStatistics,
        };
    }
}
registry.category('services').add('awesome_dashboard.statistics', AwesomeDashboardStatisticsService)
