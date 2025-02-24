/** @odoo-module **/

import { Component, markup , useState} from "@odoo/owl";
import { Counter } from "./counter/counter";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {
        Counter: Counter,
    }

    setup() {
        this.sum = useState({
            value: 2,
        });
    }

    incrementSum() {
        this.sum.value++
    }
}
