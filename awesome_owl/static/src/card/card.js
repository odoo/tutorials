import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static props = {
        label: {type: String},
        slots: {
            type: Object,
            shape: {
                default: Object,
            },
            optional: true,
        },
    };
    static template = "awesome_owl.card";

    setup() {
        this.state = useState({
            showContent: true,
        })
    }

    toggleShowContent() {
        this.state.showContent = !this.state.showContent;
    }
}
