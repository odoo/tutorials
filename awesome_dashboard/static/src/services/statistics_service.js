import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const awesome_dashboard_statistics = {
    async start() {
        this.result = await rpc('/awesome_dashboard/statistics');
        this.loadStatistics = () => this.result
        return this.loadStatistics;
    }
};

registry.category("services").add("awesome_dashboard.statistics", awesome_dashboard_statistics);
