import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { registry } from "@web/core/registry";
import { PieChart } from "./PieChart/pie_chart";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.result = useState(useService("awesome_dashboard.statistics"))
    }
    openCustomerView() {
        this.action.doAction('base.action_partner_form')
    }
    openLeadsView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "All leads",
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list', 'form']],
        });
    }

    static components = { Layout, DashboardItem, PieChart }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
