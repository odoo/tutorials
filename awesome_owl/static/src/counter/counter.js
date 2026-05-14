import { Component, useState, useRef } from "@odoo/owl";


export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        onChange: { type: Function, optional: true },
        decr: { type: Function, optional: true }
    }
    setup() {
        this.state = useState({
            value: 1,
        })
        this.limit = useState({ value: 2 })
        this.input = useRef('Input')
    }
    increment(e) {
        this.state.value++
        if (this.props.onChange) {
            this.props.onChange(e.target.innerHTML)
        }
    }
    decrement(e) {
        if (this.state.value <= 0) return;
        this.state.value--
        if (this.props.onChange) {
            this.props.onChange(e.target.innerHTML)
        }
    }
    setLimit(e) {
        if (e.keyCode == 13 && e.target.value != "") {
            this.limit.value = this.input.el.value
        }
    }
}
