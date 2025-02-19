/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter , Card}

    setup() {
        this.str1 = "<div class='text-primary'>some content</div>";
        this.str2 = markup("<div class='text-primary'>some content</div>");
    }
}
