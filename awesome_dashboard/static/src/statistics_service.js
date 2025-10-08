import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start(){
        const statistics = reactive({ isReady: false});

        async function loadData() {
            const newDatas = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, newDatas, { isReady: true });
        }

        setInterval(loadData,10000);
        loadData();

        return statistics;
    }
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
