import { Component,useState } from "@odoo/owl";


export class Card extends Component{
    static template = "awesome_owl.card";

    setup(){
        this.state = useState({isVisible: true});
    }

    static props = {
        title: String,
        slots:{
            type: Object,
            shape:{
                default:true,
            },
        }
    };

    toggleContent(){
        this.state.isVisible =!this.state.isVisible;
    }
}
