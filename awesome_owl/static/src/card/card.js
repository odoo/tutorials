import { Component,useState } from "@odoo/owl";
                                       
export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: true
            },
        },
    };

    setup() {
        this.state = useState({visible:true})
    }

    toggleContent() {
        this.state.visible = !this.state.visible
    }
}
