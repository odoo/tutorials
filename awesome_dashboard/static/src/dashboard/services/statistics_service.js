import {rpc} from "@web/core/network/rpc";
import {registry} from "@web/core/registry";
import {reactive} from "@odoo/owl";
import {browser} from "@web/core/browser/browser";

export class StatisticsService {
    constructor() {
        this.state = reactive({loaded: false});

        browser.setInterval(async () => await this._loadStatistics(), 10_000);

        const odoo = (globalThis.odoo ||= {});

        if (odoo.debug == "1") {
            browser.setTimeout(async () => await this._loadStatistics(), 2_500);
        } else {
            this._loadStatistics();
        }
    }

    async _loadStatistics() {
        const data = await rpc("/awesome_dashboard/statistics");

        Object.assign(this.state, data, {loaded: true});
    }
}

export const statisticsService = {
    start() {
        return (new StatisticsService()).state;
    }
}

registry.category("services").add("statistics", statisticsService);
