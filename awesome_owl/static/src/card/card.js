import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title : { type : String},
        slots: { type: Object, optional: true },
    }

    setup() {
        this.toggle = useState({ value : true });
    }

    onToggle() {
        this.toggle.value = !this.toggle.value;
    }
}
