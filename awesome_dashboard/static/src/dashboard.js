/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./pie_chart/pie_chart";

export class Dashboard extends Component {
    static template = "awesome_dashboard.Dashboard";
    static components = { Layout, DashboardItem, PieChart };

     setup() {
    this.actionService = useService("action");
    this.statistics = useState(useService("awesome_dashboard.statistics"));
    // this.state = useState(this.statisticsService.state);


    // onWillStart(async () => {
    //     this.state.statistics =
    //         await this.statisticsService.loadStatistics();
    // });
}

    openCustomers() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "res.partner",
            views: [[false, "list"], [false, "form"]],
        });
    }

    openLeads() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "kanban"], [false, "form"]],
        });
    }
}

registry.category("actions").add(
    "awesome_dashboard.dashboard",
    Dashboard
);

