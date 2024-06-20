/** @odoo-module **/

import { Component, markup } from "@odoo/owl";

import { Counter } from "./counter/counter.js"
import { Card } from "./card/card.js"

export class Playground extends Component {
    static template = "my_module.Playground";

    static components = { Counter, Card };
    
    card_content = markup("<a href=''>some content</a>");
}
