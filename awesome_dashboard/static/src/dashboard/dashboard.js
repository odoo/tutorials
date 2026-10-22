import "./dashboard_items";
import { Component , useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
//import { rpc } from "@web/core/network/rpc";
import { DashboardItem } from "./dashboard_item"
import { PieChart } from "./pie_chart";



class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout ,DashboardItem ,PieChart };

    setup(){
        this.action = useService("action");
        //this.statisticsService = useService("awesome_dashboard.statistics")
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();

        //onWillStart( async () => {
            //this.statistics  = await rpc("/awesome_dashboard/statistics")
           // this.statistics = await this.statisticsService.loadStatistics(); });
    }

    openCustomers(){

        this.action.doAction("base.action_partner_form");

    }

    openLeads(){

        this.action.doAction({
            type : "ir.actions.act_window",
            name : "Leads",
            res_model :"crm.lead",
            views : [ [false, "list"],[false, "form"]]
        });

    }
}

//registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
