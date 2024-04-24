/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card };

    setup(){
        this.test1 = "<div><p>Some text</p></div>";
        this.test2 = markup("<div><p>Some text</p></div>");
    }
}
