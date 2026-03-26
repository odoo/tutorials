import { markup, Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = ["title", "content"];

    setup() {
        this.state = useState({htmlLink: markup('<a href="/odoo" target="_blank">test</a>')})
    }
}
