/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { statisticsStore } from "./services/statistics_service";
import { DashboardItem } from "./dashboard_item";
import { dashboardItemRegistry } from "./dashboard_registry";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem };

    setup() {
        this.stats = useState(statisticsStore);

        // Get all registered dashboard items
        this.items = dashboardItemRegistry.getAll();
    }
}