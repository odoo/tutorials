import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "Card";
    static props = {
        title: String,
        slots: Object
    };

    setup(){
        this.state = useState( {open: true});
    }

    changeOpenState(){
        this.state.open = !this.state.open;
    }
}
