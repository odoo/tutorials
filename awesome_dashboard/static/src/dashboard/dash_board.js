import { Component } from "@odoo/owl"
import { DashboardItem } from "../dashboard_Item/dashboard_Item"
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks"

export class Dashboard extends Component {
    static template = "awesome_dashboard.dashboard"

    setup() {
        this.action = useService("action");
        this.display = {
            controlPanel: {},
        }
    }

    openSettings() {
        this.action.doAction("base_setup.action_general_configuration");
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form")
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
    static components = { Layout, DashboardItem }
}
