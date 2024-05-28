/** @odoo-module **/

import { Component , useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = { myfnc : {optional:true} };
    setup() {
        this.counter = useState({ value: 0 });
    }
    increment() {
        this.counter.value++;
        if (this.props.myfnc)  this.props.myfnc();
    }
}