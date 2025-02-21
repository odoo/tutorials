import { Component , useState } from "@odoo/owl";

export class Counter extends Component{
    static template ='awesome_owl.counter';
    static props = {
        onChange: { type: Function, optional: true }
    };
    setup(){
        this.state = useState({
            count:0
        })
    }
    increment(){
        this.state.count+=1;
        if(this.props.onChange){
            this.props.onChange();
        }
    }
}
