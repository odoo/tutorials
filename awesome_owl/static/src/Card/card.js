import { Component, useState } from "@odoo/owl";


export class Card extends Component {
    static template = "awesome_owl.card";
    static prop = {
        title : {
            type: String
        },
        content: {
            type: String,
            optional: true
        },
        slots:{
            type:Object,
            shape:{
                default:true
            }
        }
    };

    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleContent(){
        this.state.isOpen = !this.state.isOpen;
    }
}
