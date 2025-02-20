import { Component , useState ,bind } from "@odoo/owl";

export class Counter extends Component { 
    static template="awesome_owl.Counter";
    setup(){
        this.state=useState({value:0});
    }
    static props={
        sum : {type : Function,optional : true},
    }
    increment(){
        this.state.value++;
        this.props.sum();
    }
}
