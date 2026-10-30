import { Plugin, signal, onWillDestroy } from "@odoo/owl";
import { services } from "@web/core/services";
import { rpc } from "@web/core/network/rpc";

export class ReportingPlugin extends Plugin {
    stats = signal(null);

    setup() {
        this.loadData();
        const id = setInterval(() => this.loadData(), 5 * 1000);
        onWillDestroy(() => clearInterval(id));
    }

    async loadData() {
        const data = await rpc("/awesome_dashboard/statistics");
        this.stats.set(data);
    }
}

services.add(ReportingPlugin);
