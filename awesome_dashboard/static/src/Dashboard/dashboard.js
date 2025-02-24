/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem";
import { Piechart } from "./PieChart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout, Piechart }
    

    setup(){
        this.action = useService("action");
        this.display = {
            controlPanel: {},
        };
        this.state = useState([])
        this.piedata = useState({})
        this.loadStatistics =  useService("awesome_dashboard.statistics");
        this.statistics = useState(this.loadStatistics)
    }

    openCustomerView(){
        this.action.doAction("base.action_partner_form");
    }

    openLeadsView(){
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        })
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
