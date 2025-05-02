import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export const statistics = {
    start() {
        this.data = reactive({ });
        return {
            loadStatistics: this.loadStatistics.bind(this)
        };
    },
    async rpcCall() {
        const result = await rpc("/awesome_dashboard/statistics");
        for (const [key, value] of Object.entries(result)) {
            this.data[key] = value;
        }
    },
    loadStatistics() {
        if (!this.interval) {
            this.rpcCall();
            clearInterval(this.interval);
            this.interval = setInterval(this.rpcCall.bind(this), 10000);
        }
        return this.data;
    }
};

registry.category("services").add("awesome_dashboard.statistics", statistics);
