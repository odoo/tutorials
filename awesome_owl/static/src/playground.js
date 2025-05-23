/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./counter/counter.js";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter };
}
