import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./item/dashboardItem";
import { PiChart } from "./chart/piChart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PiChart }

    setup(){
        this.display = {
            controlPanel: {}
        }

    this.action = useService("action")
    this.statiscticsService = useService("awesome_dashboard.statistics_service")

    onWillStart(async () => {
        this.statistics = await this.statiscticsService.loadStatistics()
        })
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form")
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'crm leads',
            res_model: 'crm.lead',
            views: [[false,'list'], [false,'form']],
            target: 'current',
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
