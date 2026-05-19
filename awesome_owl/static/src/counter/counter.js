import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        value: { type: Number },
        callback: { type: Function }
    };

    increment () {
        this.props.callback(this.props.value + 1);
    }
    
    decrement () {
        this.props.callback(this.props.value - 1);
    }
    
    powerof () {
        this.props.callback(this.props.value ** 2);
    }
}
