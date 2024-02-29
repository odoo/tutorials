/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./Dashboard_item/Dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    async setup() {
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = items;
        console.log(this.statistics);
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        });
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
