import { Component, useState } from "@odoo/owl"

export class Card extends Component {
    // static props = {
    //     'title': String,
    //     'content': String,
    //     'slots' : Object
    // };
    static template = "awesome_owl.card";

    setup() {
        this.isOpen = useState({value: true});
    }

    toggle = () => {
        this.isOpen.value = !this.isOpen.value;
    }
}
