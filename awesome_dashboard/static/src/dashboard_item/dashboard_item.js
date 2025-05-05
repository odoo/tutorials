/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.AwesomeDashboardItem";
    static props = {
        size: {type: Number, optional: true},
        slots: {type: Object, optional: true},
    };
    static defaultProps = {
        size: 1,
    };

    setup() {
        this.width = 18 * this.props.size;
    }

    toggle() {
        this.state.open = !this.state.open;
    }
}
