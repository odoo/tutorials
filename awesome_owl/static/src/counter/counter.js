import {Component, useState} from '@odoo/owl';


export class Counter extends Component {
    static template = "counter";
    static props = {
        onChange: {type: Function, optional:true}
    }
      
    setup() {
        this.state = useState({ value: 1})

    }

    increment() {
            this.state.value++;
            if (this.props.onChange){
                this.props.onChange()
            }
    }

    decrement() {
        if(this.state.value > 0){
            this.state.value--;
        }      
        
    }
}
