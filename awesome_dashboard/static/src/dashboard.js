/** @odoo-module **/

import { Component, onWillStart, useState} from "@odoo/owl";
import { registry } from "@web/core/registry";
import {Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item"
import { rpc } from "@web/core/network/rpc";
import { PieChart } from "./pie_chart/pie_chart";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout , DashboardItem , PieChart};

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"))

        this.rpc = rpc;
        this.display = { 
            controlPanel: {},
        };
        // onWillStart(async() =>{
        //     // this.statistics = await this.rpc("/awesome_dashboard/statistics")
        //     this.statistics = await this.statistics.loadStatistics();
        // });

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



registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
