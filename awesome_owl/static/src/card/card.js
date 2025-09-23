import { Component, useState } from "@odoo/owl"

export class Card extends Component {
    static template = "awesome_owl.card"
    static props = {
        title: String,
        slots: Object,
    }

    setup() {
        this.isOpened = useState({ value: true });
    }

    toggle() {
        this.isOpened.value = !this.isOpened.value;
    }
}