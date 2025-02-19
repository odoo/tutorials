/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components= { Counter};
}
