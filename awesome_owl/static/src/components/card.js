/** @odoo-module **/

import { Component, useState } from '@odoo/owl'

export class Card extends Component{
    static template = "awesome_owl.card"
    setup(){
        this.state = useState({ isOpen: true })
    }
    static props = {
        title: { type: String },
        slots: { type: Object, optional: true}
    }

    toggleContent(){
        this.state.isOpen = !this.state.isOpen;
    }

}
