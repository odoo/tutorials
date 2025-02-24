/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "../dashboardItem/dashboardItem";
import { PieChart } from "../pieChart/pieChart";

class AwesomeDashboard extends Component {
    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"))
    }

    static template = "awesome_dashboard.AwesomeDashboard";

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    static components = { Layout, DashboardItem, PieChart }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
