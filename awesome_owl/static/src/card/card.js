/** @odoo-module **/
import { Component, markup } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";  // Capitalize "Card" to match XML
    static props = {
        title: { type: String },
        content: { type: String },
    };
    value1 = markup("<div>some text 1</div>");
    value2 = markup("<div>some <br> text 2</div>");
}
