/** @odoo-module **/

import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { Component } from "@odoo/owl";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static props = {};

    static components = { Card, Counter };
}
