/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    setup() {
        this.width = this.props.size*18
    }

    static defaultProps = {
        size: 1,
    };

    static props = {
        size: {
            type: Number,
            optional: true,
        },
        slots: {
            default: Component
        }
    };
}
