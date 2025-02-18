/** @odoo-module **/

import { Component, useState } from "@odoo/owl";


export class ChildCounter extends Component {
    static template = "awesome_owl.childCounter";
    setup() {
        this.state = useState({ value: 0 });
    } 
    increment(){
        this.state.value++;
    }
}
export class Playground extends Component {
    static template = "awesome_owl.playground";


    static components = { ChildCounter};
}

