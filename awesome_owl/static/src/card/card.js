import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    setup(){
        this.state = useState({isCollapsed: true});
    }

    static props = {
        title: { type: String, optional: true },
        slots: {
            type: Object,
            optional: true
        }
    }

    toggleContent(){
        this.state.isCollapsed = !this.state.isCollapsed;
    }

}
