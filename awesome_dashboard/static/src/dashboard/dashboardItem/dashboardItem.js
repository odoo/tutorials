import { Component, useState } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboardItem";

    static props = {
        size: { type: Number, optional: true},
        slots: { type: Object, optional: true },
    };

    static defaultProps = {
        size: 1,
    };
}
