import { Component, useState } from "@odoo/owl";


export class Card extends Component {
    static template = "awesome_owl.Card";
    setup() {
        this.state = useState({ click: true })
    }
    static props = {
        title: { type: String },
        content: { type: String, optional: true },
        pincode: { type: [Number, String] },
        slots: {
            type: Object,
            optional: true,
            shape: {
                default: { optional: true }
            },
        }
    }
    clicked() {
        this.state.click = !this.state.click
    }
}
