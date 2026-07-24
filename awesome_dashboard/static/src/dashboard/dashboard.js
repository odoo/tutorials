import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statistics = useService("statistics");
        this.stats = this.statistics.onUpdate;

        onWillStart(async () => {
            const result = await this.statistics.loadStatistics();
            // WARN; Perform immediate/synchronous update of state because sub-components
            // logic isn't safeguarded against undefined values.
            for (const [key, value] of Object.entries(result)) {
                this.stats[key] = value;
            }
        });
    }

    async openCustomers() {
        this.action.doAction("base.action_partner_form", {});
    }

    async openLeads() {
        this.action.doAction("crm.crm_lead_all_leads");
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
