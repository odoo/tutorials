import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from '@web/search/layout'
import { DashboardItem } from "./dashboardItem";
import { PieChart } from "./pie_chart/pie_chart";
import "./statistics_service";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboardView";
    static components = { Layout,DashboardItem,PieChart }

    setup(){
        this.action = useService("action")
        this.statisticsService = useService(
            "awesome_dashboard.statistics"
        );
        this.state = useState({
            data:{}
        })
        onWillStart(async()=>{
            const data = await this.statisticsService.loadStatistics();
            this.state.data = data
            console.log(this.state.data,data);
            
            // this.statistics.set(data);
        })
    }
    openCustomers(){
        this.action.doAction("base.action_partner_form")
    }
    openLead() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
