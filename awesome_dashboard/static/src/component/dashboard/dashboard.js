/** @odoo-module */

import { Component, onWillStart } from '@odoo/owl';
import { Layout } from '@web/search/layout';
import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';
import { DashboardItem } from '../dashboardItem/dashboard_item';
import { rpc } from '@web/core/network/rpc';

class AwesomeDashboard extends Component {
    static template = 'awesome_dashboard.AwesomeDashboard';
    static components = { Layout, DashboardItem };
    setup() {
        this.actionService = useService('action');
        this.helloService = useService('hello_service');   
        this.stats = {
            newOrders: 0,
            totalAmount: 0,
            avgTShirtOrder: 0,
            cancelledOrders: 0,
            avgOrderTime: 0,
        };  
        onWillStart(async () => {
            const result = await rpc('/awesome_dashboard/statistics');
            this.stats = {
                newOrders: result.nb_new_orders,
                totalAmount: result.total_amount,
                avgTShirtOrder: result.average_quantity,
                cancelledOrders: result.nb_cancelled_orders,
                avgOrderTime: result.average_time,
            };
        });   
    }
    openCustomers() {
        this.actionService.doAction('base.action_partner_form');
    }
    openLeads() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            view_mode: 'list',
            views: [[false, 'list'], [false, 'form']], 
            target: 'current',
        }); 
    }
}
registry.category('actions').add('awesome_dashboard.dashboard', AwesomeDashboard);
