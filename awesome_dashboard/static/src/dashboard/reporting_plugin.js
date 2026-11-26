import { signal, Plugin, onWillDestroy } from "@odoo/owl";
import { services } from "@web/core/services";
import { rpc } from "@web/core/network/rpc";


export class ReportingPLugin extends Plugin {

    statistics = signal(null)

    setup() {
        this.loadStatistics()
        const id = setInterval(() => this.loadStatistics(), 5000)
        onWillDestroy(() => clearInterval(id))
    }

    async loadStatistics() {
        const result = await rpc("/awesome_dashboard/statistics", {}, { cache: true })
        this.statistics.set(result)
    }

}

services.add(ReportingPLugin)
