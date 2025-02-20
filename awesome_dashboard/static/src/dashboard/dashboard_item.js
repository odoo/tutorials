/** @odoo-module **/
import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        slots: {
            type: Object,
            shape : {
                default: true
            },
        },
        size: {
            type: Number,
            optional: true,
        },
    };
    static defaultProps = {
        size: 1,
    };
}