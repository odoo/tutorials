/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
// import { sharedCounter } from "../store"; 

export class Counter extends Component {
    static template = "awesome_owl.counter"

    static props = {
        onChange: { type: Function, optional: true },
    }

    setup() {
        this.state = useState({
            value: 0,
        })
    }
    
    increment() {
        this.state.value++
        if (this.props.onChange) {
            this.props.onChange(this.state.value)
        }
    }
}


// export class Counter extends Component {
//     static template = "awesome_owl.counter";
//     static props = {
//         id: { type: Number },
//     };
    
//     setup() {
//         this.state = useState(sharedCounter);
//     }
    
//     increment() {
//         if (this.props.id === 1) {
//             // Counter 1 only increments itself
//             this.state.counter1++;
//         } else if (this.props.id === 2) {
//             // Counter 2 increments both counters
//             this.state.counter1++;
//             this.state.counter2++;
//         }
//     }
    
//     get value() {
//         return this.props.id === 1 ? this.state.counter1 : this.state.counter2;
//     }
// }
