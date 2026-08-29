import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = ["title", "slots?"]

    setup() {
        this.open = useState({ value: true });
    }
    
    toggleOpen() {
        this.open.value = !this.open.value
    }
}
