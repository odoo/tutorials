/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card };

    setup() {
        this.content = "<div>some content</div>";
        this.content2 = markup("<div>some content</div>");
    }
}
