import { Component } from "@odoo/owl";


export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        title: { type: String, required: true },
        value: { type: Number, required: true },
    };

    setup() {
        this.state = { title: this.props.title, value: this.props.value };
    }

}
