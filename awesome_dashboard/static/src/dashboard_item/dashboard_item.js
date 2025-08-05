import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_owl.dashboard_item";

    static props = {
        size: { type: Number, optional: true },
        slots: { type: Object }
    }

    static defaultProps = {
        size: 1
    }

}
