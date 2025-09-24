import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { dashboardItemRegistry } from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, NumberCard, PieChartCard };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("statistics");
        this.state = useState(this.statisticsService);
        this.items = dashboardItemRegistry.getAll();
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Leads",
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
