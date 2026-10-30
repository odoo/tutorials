import { Plugin, signal, onWillDestroy } from "@odoo/owl"
import { rpc } from "@web/core/network/rpc";
import { services } from "@web/core/services";



export class ReportingPlugin extends Plugin {

    stats = signal(null);
    counter = null

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