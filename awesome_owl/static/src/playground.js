/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        this.content_1 = "<div class='text-primary'>some content</div>";
        this.content_2 = markup("<div class='text-primary'>some content</div>");
    }
    static components = { Counter, Card };
}
