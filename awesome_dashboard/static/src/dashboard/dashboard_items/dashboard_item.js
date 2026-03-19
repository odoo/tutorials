import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: {
            type: Object,
            optional: true,
        },
        slots: {
            type: Object,
            optional: true,
        },
    };
    static defaultProps = {
        size: 1,
    };

    setup() {
        super.setup();
    }
}
