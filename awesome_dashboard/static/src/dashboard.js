/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.display = {controlPanel: {}};
        this.stats = useState(useService("awesome_dashboard.statistics"));
        this.action = useService("action");
    }

    viewCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    viewLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'All leads',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
