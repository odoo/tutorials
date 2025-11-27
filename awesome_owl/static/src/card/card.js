import { Component, useState, Slot } from "@odoo/owl";


export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: {type: String},
        slots : { type: Object, optional: true },
    }
    setup(){
        this.state = useState({ show: false });
    }

    toggleShow(){
        this.state.show = !this.state.show;
    }
}
