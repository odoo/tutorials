/** @odoo-module **/

import { Component, markup , useState} from "@odoo/owl";
// import { Counter } from "./counter/counter";
import { Card } from "./card/card.js";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {
        // Counter: Counter,
        Card: Card,
    }
    
}
