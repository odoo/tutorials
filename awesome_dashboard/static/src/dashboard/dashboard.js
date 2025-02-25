/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { rpc } from '@web/core/network/rpc';
import { dashboardItems } from "./dashboard_items";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup(){
        this.action = useService("action");
        // this.stats = null;
        this.statisticsService = useService("statistics");

        // onWillStart(async () => {
        //     this.stats = await rpc("/awesome_dashboard/statistics");
        // })

        // Fetch statistics only when the component is first mounted
       /*  onWillStart(async () => {
            this.stats = await this.statisticsService.loadStatistics();
            // console.log(this.stats);
            
        }); */


        this.stats = useState(this.statisticsService.stats);

        this.items= registry.category("awesome_dashboard.items").getAll();
        
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            target: "current",
            views: [[false,"list"],[false,"form"]],
        });
    }


}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
