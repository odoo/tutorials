import { Component, useState } from "@odoo/owl";


export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: {}
            }
        }
    };

    setup() {
        this.state = useState({visible: true})
    }

    toggleContent() {
        this.state.visible = !this.state.visible;
    }
}
