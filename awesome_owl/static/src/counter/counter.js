import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        onChange: { type: Function, optional: true },
        increment:{ type: Boolean, optional: true}
    }

    setup() {
        this.counter = useState({ value : 0 })
    }
    
    onCalculate(operator) {
        if (operator === '+') {
            this.counter.value++;
            if (this.props.onChange) {
                this.props.onChange(operator);
            }
        }
        else {
            this.counter.value--;
            if (this.props.onChange) {
                this.props.onChange(operator);
            } 
        }
        
    }
}
