/** @odoo-module **/

import { Layout } from "@web/search/layout";
import { Component, useState, onWillStart} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./piechart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));
    }

    displayCustomerKanban() {
        this.action.doAction("base.action_partner_form")
    }

    displayLeads() {

        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false,'tree']],
        });
    }

}

registry.category("lazy_components").add("awesome_dashboard", AwesomeDashboard);