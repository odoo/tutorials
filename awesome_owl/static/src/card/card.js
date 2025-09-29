import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: String,
        slots: { type: Object, optional: true },
    };

    setup() {   
        this.state = useState({contentState: true});
    }

    toggleContent(){
        this.state.contentState = !this.state.contentState;
    }
}
