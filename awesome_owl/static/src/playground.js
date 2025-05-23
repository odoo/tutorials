/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter.js";
import { Card } from "./card/card.js";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    raw_card_title = "<u>Hello</u>";
    raw_card_text = "<u>World</u>";

    card_title = markup(this.raw_card_title);
    card_text = markup(this.raw_card_text);
}
