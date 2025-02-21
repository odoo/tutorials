/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import {DashboardItem} from "./dashboard_item/dashboard_item"
import { Layout } from "@web/search/layout";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {DashboardItem, Layout, PieChart}

    setup(){
        this.action = useService("action");
        this.display = {
            controlPanel : {}
        }
        this.statistics_data = useState(useService("awesome_dashboard.statistics"))
    }

    openCustomerView(){
        this.action.doAction("base_setup.action_general_configuration")        
    }

    openCrmLeadView(){
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views: [
                [false, 'list'],
                [false, 'form']
            ]
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
