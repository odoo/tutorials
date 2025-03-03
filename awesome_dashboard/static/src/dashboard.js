/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout }

    setup(){
        this.action = useService("action")
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
