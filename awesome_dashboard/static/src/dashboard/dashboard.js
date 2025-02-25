import { Component,useState } from "@odoo/owl";
import { DashboardItem } from "./dashboardItem";
import { items } from "./dashboard_item";
import { Layout } from "@web/search/layout"
import { PieChart } from "./PieChart";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout , DashboardItem,PieChart}
    setup(){
    this.action= useService('action')
    this.statisticsService = useService("awesome_dashboard.statistics");
    this.stats = useState(this.statisticsService.stats);
    this.items=items;
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
registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard,{force : true});
