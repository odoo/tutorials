import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: { type: String },
        slots: Object,
    };

    setup() {
        this.show = useState({ value: true });
    }

    toggleShow() {
        this.show.value = !this.show.value;
    }
}

