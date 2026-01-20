import { Component, useState, onWillDestroy } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        onChange: { type: Function, optional: true }
    };

    setup(){
        console.log("Counter created");
        this.state = useState({ value: 0 });
        onWillDestroy(() => {
            console.log("Counter will be destroyed");
        });
    }

    increment(){
        this.state.value++;
        if(this.props.onChange){
            this.props.onChange();
        }
        
    }
}

