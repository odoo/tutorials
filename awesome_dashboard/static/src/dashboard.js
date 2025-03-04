/** @odoo-module **/

import { Component, onWillStart, useState } from '@odoo/owl';
import { DashBoardItem } from './dashboarditem/dashboarditem';
import { Layout } from '@web/search/layout';
import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';

export class AwesomeDashboard extends Component {
    static template = 'awesome_dashboard.awesomedashboard';
    static components = { Layout, DashBoardItem }

    setup(){
        this.action = useService('action');
        this.awesome_dashboard_statistics = useService("awesome_dashboard.statistics")
        this.result = useState(this.awesome_dashboard_statistics());
    }

    openCustomers(){
        this.action.doAction('base.action_partner_form');
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'form']]
        });
    }
}

registry.category('actions').add('awesome_dashboard.dashboard', AwesomeDashboard);
