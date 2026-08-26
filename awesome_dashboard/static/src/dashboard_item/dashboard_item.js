import { Component, useState } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_owl.dashboard_item";
    static props = {
        title: String,
        size: { type: Number, optional: true },
        slots: {
            type: Object,
            optional: true,
            shape: {
                default: { optional: true },
            },
        },
    };

    static defaultProps = {
        size: 1
    }

    setup() {
    }

    get cardWidth() {
        return 18 * this.props.size;
    }

}
