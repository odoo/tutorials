import { Component, useState, xml } from "@odoo/owl";


export class Counter extends Component {
    static props = ['onChange?']

    static template = xml`
    <t t-esc="state.value"/>
    <button t-on-click="increment">Press</button>
    `

    setup(){
        this.state = useState({value: 1});
    }

    increment(){
        this.state.value += 1;
        if (this.props.onChange){
            this.props.onChange()
        }
    }
}
