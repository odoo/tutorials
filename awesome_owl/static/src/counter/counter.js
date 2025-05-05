import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onchange : {type: Function, optional: true},
    };
    
    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value += 1;
        console.log(this.props.onchange());
        if(this.props.owlnchange){
            this.props.onchange();
        }
    }
}

