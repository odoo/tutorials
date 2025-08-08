import { Component , useState } from "@odoo/owl";
import {Counter} from './counter/counter';
export class Card extends Component { 
    static template="awesome_owl.Card";
    static components={Counter};
    static props={
        title : {type : String},
        content : {type : String,optional:true},
        slots : {type : Object , 
            shape : {default : true}
        }
    }
    setup(){
        this.toggle=useState({isOpen:true});
    }
    toggleAct(){
        this.toggle.isOpen = !this.toggle.isOpen;
    }
}
