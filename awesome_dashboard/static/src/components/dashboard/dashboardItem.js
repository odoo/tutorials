import { Component } from "@odoo/owl";


export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: { type: Number, default: 1, optional: true },
        content: { type: String, optional: true },
        slots: { type: Object, optional: true },
    };

    setup() {
        this.state = { size: this.props.size, width: 18*this.props.size , content: this.props.content };
    }

}
