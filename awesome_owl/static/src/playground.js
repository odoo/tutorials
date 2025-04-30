/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    card1Content = markup("<div>Some Text in div Tag</div>");
    card2Content = "<div>Some Text in div Tag</div>";
}