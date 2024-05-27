/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Reactive } from "@web/core/utils/reactive";

const TEN_MINUTES = 10 * 60 * 1000;

class StatisticsStore extends Reactive {
    static serviceDependencies = ["rpc"];

    constructor() {
        super();
        this.setup(...arguments);
    }

    setup(env, { rpc }) {
        this.rpc = rpc;

        this.orders_by_size = {};

        this._loadStatistics();
        setInterval(async () => await this._loadStatistics(), TEN_MINUTES);
    }

    async _loadStatistics() {
        const newData = await this.rpc("/awesome_dashboard/statistics");
        Object.assign(this, newData);
    }
}

export const statisticsService = {
    dependencies: ["rpc"],
    start() {
        return new StatisticsStore(...arguments);
    }
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
