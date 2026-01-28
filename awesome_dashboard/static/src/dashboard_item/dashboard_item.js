import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: { type: Number, optional: true },
        slots: {
            type: Object,
            shape: { default: Object },
        },
    };

    static defaultProps = {
        size: 1,
    };
}
