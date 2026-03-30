import { markup, Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: {
            type: String,
            optional: true,
        }, 
        slots: {
            type: Object,
            optional: true,
        }, 
    };

    setup() {
        this.state = useState({htmlLink: markup('<a href="/odoo" target="_blank">test</a>')})
        this.isMinimized = useState({value: false});
    }

    toggle() {
        this.isMinimized.value = !this.isMinimized.value;
    }
}
