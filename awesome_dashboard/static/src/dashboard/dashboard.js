/** @odoo-module **/

import { Component, onWillStart, useState } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { Layout } from '@web/search/layout';
import { useService } from '@web/core/utils/hooks';
import { DashboardItem } from './dashboard_item/dashboard_item';
import { PieChart } from '../pie_chart/pie_chart';

class AwesomeDashboard extends Component {
    static template = 'awesome_dashboard.AwesomeDashboard';
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.showCustomers = this.showCustomers.bind(this);
        this.showLeads = this.showLeads.bind(this);
        this.action = useService('action');
        this.stats = useState(useService('awesome_dashboard.statistics'));
    }

    showCustomers() {
        this.action.doAction('base.action_partner_form');
    }

    showLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
        });
    }
}

registry
    .category('lazy_components')
    .add('AwesomeDashboard', AwesomeDashboard);
