import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_dashboard.card";
    static props = {
        size: Number,
        slots: Object
    };
    static defaultProps = {
        size: 1
    }

    setup() {
        this.size = this.props.size * 18;
    }
}
