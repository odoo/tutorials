/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { AwesomeDashboardItem } from "./dashboard_item/dashboard_item"
import { PieChart } from "./pie_chart/pie_chart";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = {Layout, AwesomeDashboardItem, PieChart}

    setup() {
        this.action = useService("action");
        this.statistic = useState(useService("awesome_dashboard.statistics"))
        this.display = {
            controlPanel: {},
        };
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);