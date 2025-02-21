/** @odoo-module **/

import { useState, Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./DashboardItem/dashboard_item";
import { PieChart } from "./PieChart/pie_chart";

class AwesomeDashboard extends Component {
    static components = { DashboardItem, Layout, PieChart };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.statistics);
        this.items = registry.category("awesome_dashboard").getAll();
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction("crm.crm_lead_all_leads");
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
