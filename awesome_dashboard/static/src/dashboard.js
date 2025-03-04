/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks"
import { rpc } from "@web/core/network/rpc"
import { DashboardItem } from "./dashboarditem/dashboarditem";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup(){
        this.result = useState({data: null})
        this.action = useService("action")
        onWillStart(async()=>{
            this.result.data = await rpc("/awesome_dashboard/statistics")
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
