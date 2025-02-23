/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks"
import { DashBoardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashBoardItem, PieChart}
    setup(){
        this.action = useService("action")
        this.statsService = useService("awesome_dashboard.statistics")
        this.stats = useState(this.statsService.stats)
        console.log(this.stats)
        this.display = {
            controlPanel: {}
        }
    }

    onClickCustomers(){
        this.action.doAction("base.action_partner_form")
    }

    onClickLeads(){
        this.action.doAction({
            "type": "ir.actions.act_window",
            "name": "All Leads",
            "res_model": "crm.lead",
            "views": [[false, "list"],[false, "form"]]
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
