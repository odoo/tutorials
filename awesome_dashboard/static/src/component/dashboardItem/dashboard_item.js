/** @odoo-module */

import { Component } from '@odoo/owl';

export class DashboardItem extends Component {
    static template = 'awesome_dashboard.dashboardItem';
    static defaultProps = {
        size: 1,
    };
    static props = { 
        size: { type: Number, optional: true},
        slots: { type: Object }, 
        value: { type: Number, optional: true },
    };
}
