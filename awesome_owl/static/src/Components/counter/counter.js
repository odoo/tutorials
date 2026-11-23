import {Component, useState } from "@odoo/owl";

export class Counter extends Component{
    static template = "awesome_owl.Counter";
     setup(){
        this.state=useState({value:0})
     }
     static props ={
        onSum:{type:Function, optional: true},
        onDecrese: {type: Function, optional:true}
     }
     increment(){
        this.state.value++;
        if (this.props.onSum){
            this.props.onSum()
        }
     }
     decrement()
     {
        if (this.state.value >0)
        {
            this.state.value--;
            if (this.props.onDecrese)
            {
                this.props.onDecrese()
            }
        }
     }
}