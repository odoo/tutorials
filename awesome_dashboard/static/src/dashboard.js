/** @odoo-module **/
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from '@web/search/layout'
import { DashboardItem } from "./dashboard_item/dashboard_item";
import {PieChart} from "./pie_chart/pie_chart";
import {DashboardItemContent} from "./dashboard_item_content/dashboard_item_content";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart, DashboardItemContent}

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("statistics"));
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeadView() {
        this.action.doAction({
            type: "ir.actions.act_window",
            mane: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
