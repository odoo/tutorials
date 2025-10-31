/** @odoo-module **/

import { Component, useState } from '@odoo/owl'


export class Card extends Component{
    static template = "awesome_owl.card"
    static props = ['slots']

    setup(){
        this.state = useState({isToggled: true});
    }

    toggle() {  
        console.log(this.state.isToggled)
        this.state.isToggled = !this.state.isToggled;
    }
}
