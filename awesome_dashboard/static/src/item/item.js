import { Component, useState } from "@odoo/owl";

export class Item extends Component {
    static props = {
        size: { type: Number, optional: true },
        slots: { type: Object, optional: true }
    }

    static template = "awesome_dashboard.item"
    setup() {
        if (!this.props.size) {
            this.props.size = 1;
        }
        this.state = useState({ size: (18 * this.props.size).toString().concat("rem") })
    }
}
