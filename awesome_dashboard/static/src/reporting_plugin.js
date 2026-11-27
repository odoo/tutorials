import { Plugin, signal } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { services } from "@web/core/services";

export class ReportingPlugin extends Plugin {

    stats = signal(null);

    async loadStatistics() {
        const data = await rpc("/awesome_dashboard/statistics", {}, { cache: true });
        this.stats.set(data);
    }
}

services.add(ReportingPlugin)
