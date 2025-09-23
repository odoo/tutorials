import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem"

    static props = {'size': {type: Number, optional: true }}

    setup() {
        if(!this.props.size) {
            this.props.size = 1
        }
    }
}
