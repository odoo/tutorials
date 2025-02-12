/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.playground";
  
     static template = xml``
    
}
export class Counter extends Component { 

    setup() {
        this.state = useState({ value: 0 });
    }
    increment() {
        this.state.value++;
    }
}
