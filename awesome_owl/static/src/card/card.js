import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: {type: String, validate: val => {
            if(val.length === 0) return false;

            let first = val.substring(0, 1);
            return first === first.toUpperCase();
        }},
        slots: {type: Object, optional: true},
    }

    setup() {
        this.state = useState({open: true});
    }

    toggle(){
        this.state.open = !this.state.open;
    }
}
