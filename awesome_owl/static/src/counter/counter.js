import { Component, useState, onMounted } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        start: Number,
        onChange: Function,
        totalSum: Function,
    }
    setup() {
        this.state = useState({ value: this.props.start });
        onMounted(() => {
            this.props.totalSum(this.props.start);
        });
    }
    
    increment() {
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange(0);
        }
    }
    decrement() {
        if(this.state.value == 0){
            alert("Counter's value is negative!!")
            return
        }
        if (this.props.onChange) {
            this.props.onChange(1);
        }
        this.state.value--;
    }
}
