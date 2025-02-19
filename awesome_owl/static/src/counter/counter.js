/** @odoo-module **/

import { useState, Component, xml } from "@odoo/owl"

export class Counter extends Component {
    static props = {
        onChange: {
            type: Function,
            optional: true
        }
    }

    static template = xml`
     <div class="d-inline-block border border-1 ms-3 p-2">
         <span>Counter: <t t-esc="counterState.counter"/></span>
         <button class="btn btn-primary text-white ms-3" t-on-click="increment" t-on-change="onChange"  style="background-color:#a64dff;">Increment</button>
     </div>
    `;
    counterState = useState({ counter: 1 });

    increment() {
        this.counterState.counter++;
        if (this.props.onChange) this.props.onChange()
    }
}

