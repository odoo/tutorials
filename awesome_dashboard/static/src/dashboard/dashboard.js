import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { registry } from "@web/core/registry";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.result = useState(useService("awesome_dashboard.statistics"))
        this.items = registry.category('awesome_dashboard').getAll()
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

    static components = { Layout, DashboardItem }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
