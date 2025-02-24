/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem";
import { PieChart } from "./piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart};

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics")
        this.statistics = useState(this.statisticsService.data);

    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, 'list'],[false, 'form']],
            target: "current",
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
