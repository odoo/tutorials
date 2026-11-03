import { Plugin, signal, onWillDestroy } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { services } from "@web/core/services";

export class ReportingPlugin extends Plugin {
    stats = signal(null);

    setup() {
        this.loadStatistics();
        this.timeInterval = setInterval(() => this.loadStatistics(), 10 * 1000); // * 60
        onWillDestroy(() => {
            clearInterval(this.timeInterval);
        });
    }

    async loadStatistics() {
        this.stats.set(await rpc("/awesome_dashboard/statistics", {}, { cache: true }));
    }
    
}
services.add(ReportingPlugin);
