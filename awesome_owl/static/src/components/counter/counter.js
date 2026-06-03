import { Component,useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    setup(){
        this.state = useState({value : 0});
    }
    static props = {
    onButtonClick: {
        type: Function,
        optional: true,
    },
    sum: {
        type: Number,
        optional: true,
    },
};
    increment(){
        this.state.value ++;
    } 
    decrement(){
        this.state.value --;
    } 
     reset(){
        this.state.value = 0;
    } 
     multiply(){
        this.state.value *= this.state.value;
    } 

    handleIncrement(){
        if(this.props.onButtonClick){
            this.props.onButtonClick();
            this.increment();
        }
    }

}
