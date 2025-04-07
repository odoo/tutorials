import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions"; 
import { reactive } from "@odoo/owl";

const statistics = {
    dependencies: [],
    start() {

        const stats = reactive({ data: null });

        const loadStatistics = memoize( async () => {
            const result = await rpc("/awesome_dashboard/statistics");
            stats.data = result;
        })

        loadStatistics();

        setInterval(() => {
            loadStatistics();
        }, 10000);
        

        return {
            stats
        };
    }
};

registry.category("services").add("awesome_dashboard.statistics", statistics);
