import { Component } from "@odoo/owl";


export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem"
    static props = {
        size: { type: Number, optional: true, default: 1},
    }

    get widthStyle() {
        return `width: ${18 * this.props.size}rem;`;
    }


}
