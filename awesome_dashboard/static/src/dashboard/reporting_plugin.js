import { onWillDestroy, Plugin, signal } from "@odoo/owl";
import { services } from "@web/core/services";
import { rpc } from "@web/core/network/rpc";

export class ReportingPlugin extends Plugin {
    reload_per_seconds = 10 * 60;  // 10 minutes
    stats = signal(null);

    setup() {
        this.loadStatisticsOnce();
        const timer = setInterval(() => {
            this.loadStatisticsOnce();
        }, this.reload_per_seconds * 1000
        );
        onWillDestroy(() => {
            clearInterval(timer);
        });
    }

    async loadStatisticsOnce() {
        const data = await rpc("/awesome_dashboard/statistics");
        this.stats.set(data);
    }
}

services.add(ReportingPlugin);
