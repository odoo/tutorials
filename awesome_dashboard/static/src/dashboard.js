/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
    }

    async openCustomers() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'res.partner',
            views: [[false, 'kanban']],
        });
    }

    async openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            name: 'Leads',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
