/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem";
import { PieChart } from "./piechart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    setup() {
        this.action = useService("action");
        this.stats = useService("awesome_dashboard.statistics");
        this.stats = useState(this.stats.stats)

        this.display = {
            controlPanel: {},
        };
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }   

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false ,"form"],[false ,"list"]],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
