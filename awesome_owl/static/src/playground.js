/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter , Card}
    setup() {
        this.html = "<div class='text-primary'>Some Content</div>";
        this.Markuphtml = markup("<div class='text-primary'>Some Content</div>");
    }

}
