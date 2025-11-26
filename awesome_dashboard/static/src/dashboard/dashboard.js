import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout, PieChart };

    setup() {
        this.action = useService("action");
        this.statisticService = useService("statistics");
        this.statistics = useState(this.statisticService);
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
