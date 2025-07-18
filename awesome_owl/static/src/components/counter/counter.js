import { Component, useState } from "@odoo/owl"

export class Counter extends Component{
    static template = "awsome_owl.Counter"
    static props = {
        onChange: {type: Function, optional: true}
    }

    setup(){
        this.info = { message: "Hello from Card!" };
        this.state = useState({ count:0 });

    }
    
    increment(){
        this.state.count++;

        if(this.props.onChange){
            this.props.onChange()
        }
    }
}