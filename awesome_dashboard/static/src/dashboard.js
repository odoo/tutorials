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
        this.stats = useState({});

        onWillStart(async () => {
            const result = await this.statistics.loadStatistics();
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

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
