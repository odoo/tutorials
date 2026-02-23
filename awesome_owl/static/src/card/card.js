import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";

    static props = {
        title: String,
    };

    setup() {
        this.state = useState({
            showContent: true,
        });
    }

    toggleContent() {
        this.state.showContent = !this.state.showContent;
    }
}