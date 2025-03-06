/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks"
import { DashboardItem } from "./components/dashboarditem/dashboarditem";
import { PieChart } from "./components/piechart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    setup(){
        this.result = useState({data: null})
        this.action = useService("action")
        this.statistics = useService("awesome_dashboard.statistics")
        onWillStart(async()=>{
            this.result.data = await this.statistics.loadStatistics()
        })
    }

    opoenCustomers(){
        this.action.doAction("base.action_partner_form")
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false,'list'],[false,'form']]
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
