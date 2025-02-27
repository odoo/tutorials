import { Component, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";

export class Card extends Component{
    static template = "awesome_owl.card_template"
    static components = { Counter }
    static props = { 
        title: {type: String, optional:false}
    }
    state = useState({ isOpen:true })

    change(){
        this.state.isOpen = !this.state.isOpen
    }
}
