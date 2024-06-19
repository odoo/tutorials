/** @odoo-module **/

import { Component } from "@odoo/owl";

import { Counter } from "./counter/counter.js"

export class Playground extends Component {
    static template = "my_module.Playground";

    static components = { Counter };
}
