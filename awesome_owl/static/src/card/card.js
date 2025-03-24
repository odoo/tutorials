/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";  // Link to card.xml template
    static props = ["title", "content"];   // Define props
}
