/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./counter/counter";

export class Playground extends Component {
    static template = "owl_playground.playground";

    static components = { Counter };
}
