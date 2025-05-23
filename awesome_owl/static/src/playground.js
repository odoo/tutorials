/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./counter/counter.js";
import { Card } from "./card/card.js";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };
}
