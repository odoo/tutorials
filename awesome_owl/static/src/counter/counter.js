import { Component, useState } from '@odoo/owl'

export class Counter extends Component {
    static template = 'awesome_owl.counter';
    static props = {
        'value': {type: Number, optional: true},
        'onChange': {type: Function, optional: true},
    };

    setup(){
        let temp = 0
        if(this.props['value']){
            temp = this.props.value;
        }
        this.state = useState({value: temp})
    }

    increment(){
        this.state.value++;
        this.props.onChange?.();
    }
}
