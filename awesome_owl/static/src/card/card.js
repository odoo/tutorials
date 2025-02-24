import { Component, useState } from "@odoo/owl";

export class Card extends Component{
    static template = "awesome_owl.card";

    setup(){
        this.isOpen = useState({value:true})
    }

    static props = {
        title : String,
        slots: { type: Object}
    }

    toggleContent(){
        this.isOpen.value = !this.isOpen.value
    }
}
