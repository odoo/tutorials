/** @odoo-module **/

import { Component} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    
    setup() {
        this.title = this.props.title;
        this.content = this.props.content;
    }

    onClick() {
     console.log(`Card ${this.title} clicked`)
    }
}