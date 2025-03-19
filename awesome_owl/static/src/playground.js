/** @odoo-module **/

import { Component, markup , useState} from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {
        Card,
        Counter
    }
}
