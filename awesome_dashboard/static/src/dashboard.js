import { Component,onWillStart,useState } from "@odoo/owl";
import { Layout } from "@web/search/layout"
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout , DashboardItem}
    setup(){
    this.action= useService('action')
    this.statisticsService = useService("awesome_dashboard.statistics");
    this.stats= {}
    onWillStart(async () => {
        this.stats = await this.statisticsService.loadStatistics();
        console.log(this.statistics)
    });
    }
    openCustomers(){
        this.action.doAction('base.action_partner_form')
    }
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: ("Leads"),
            res_model: "crm.lead",
            target: "current",
            views: [[false,'list'],[false,'form']]
        });
    }
}
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
