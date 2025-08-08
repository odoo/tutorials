/** @odoo-module **/

import { Component } from '@odoo/owl';

export class DashboardItem extends Component{
    static template = 'awesome_dashboard.DashboardItem';

    static props = {
        size: {
            type: Number,
            optional: true,
        },
    };

    static defaultProps = {
        size: 1,
    };

    setup() {
        this.size = this.props.size || 1;
    }
}
