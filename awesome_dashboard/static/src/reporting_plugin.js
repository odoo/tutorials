import { Plugin } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { services } from "@web/core/services";

export class ReportingPlugin extends Plugin {

    loadStatistics() {
        return rpc("/awesome_dashboard/statistics", {}, { cache: true });
    }
}

services.add(ReportingPlugin)
