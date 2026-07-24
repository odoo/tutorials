import { Component,useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    setup(){
        this.state=useState({value:1})
    }
    increament(){
        this.state.value++;
    }

    increamentt(){
        this.state.value+=2;
    }
    reset(){
        this.state.value=1;
    }
}
