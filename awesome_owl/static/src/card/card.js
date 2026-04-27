import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";

    setup(){
        this.state = useState({
            isOpen: true,
        });
    }

    toggle() {
        this.state.isOpen = !this.state.isOpen;
    }

    static props = {
        title : String,
        slots: Object,
    }
}
