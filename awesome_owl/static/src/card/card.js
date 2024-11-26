import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title : String,
        slots : {type: Object, optional: true}
    }
    setup() {
        this.opened = useState({ value: false });
    }

    toggle() {
        this.opened.value = !this.opened.value;
    }

  }
