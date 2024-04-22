/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter"
import { Card } from "./card"
export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card }

    setup(){
        html = "<div> This is a dev </div>";
        html_markup = markup(this.html);
    }
}
