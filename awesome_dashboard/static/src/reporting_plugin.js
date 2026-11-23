import { Plugin } from "@odoo/owl";
import { services } from "@web/core/services";
import { rpc } from "@web/core/network/rpc";

export class ReportingPlugin extends Plugin {
    loadStatistics() {
        return rpc("/awesome_dashboard/statistics", {}, { cache: true });
    }
}

services.add(ReportingPlugin);
