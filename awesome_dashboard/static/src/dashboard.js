/** @odoo-module **/

import { Component } from '@odoo/owl';
import { DashBoardItem } from './dashboarditem/dashboarditem';
import { Layout } from '@web/search/layout';
import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';

export class AwesomeDashboard extends Component {
    static template = 'awesome_dashboard.awesomedashboard';
    static components = { Layout, DashBoardItem }

    setup(){
        this.action = useService('action');
    }

    openCustomers(){
        this.action.doAction('base.action_partner_form');
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'form']],
        });
    }
}

registry.category('actions').add('awesome_dashboard.dashboard', AwesomeDashboard);
