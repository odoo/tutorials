import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card"

    static props = {
        title: String,
        slots: Object
    }

    setup() {
        this.isOpen = useState({ value: true })
    }

    toggleOpen() {
        this.isOpen.value = !this.isOpen.value
    }
}
