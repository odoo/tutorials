/** @odoo-module **/

import { Component } from '@odoo/owl';

export class DashBoardItem extends Component {
    static template = 'awesome_dashboard.dashboarditem';
    static defaultProps = {
        size: 1
    };
    static props = {
        size: {
            type: Number,
            optional: true,
        },
      }
}
