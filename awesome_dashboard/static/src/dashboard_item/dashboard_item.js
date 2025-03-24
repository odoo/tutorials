import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = 'dashboard_item.dashboard_item';
    static props = {
        size: {type: 'Number', optional: 'true',},
        slots: {type: 'Object', optional: 'true',},
    }

    setup() {
        this.size = this.props.size ? this.props.size : 1;
    }
}
