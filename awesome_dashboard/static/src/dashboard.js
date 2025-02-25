/** @odoo-module **/

import { Component, onWillStart, useState, useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import {Layout} from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { PieChart } from "./pie_chart/pie_chart";
import { reactive } from "@odoo/owl";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart};

    setup(){
        this.action = useService("action");
        this.statisticsService = useState(useService("awesome_dashboard.statistics"));
        this.state = reactive({ statistics: {} });        

        onWillStart(async () => {
            this.state.statistics = await this.statisticsService.loadStatistics();
        });

        useEffect(() => {
            this.state.statistics = this.statisticsService.statistics.data;
        });
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, 'form'], [false, 'list']]
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
