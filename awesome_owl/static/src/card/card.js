import { Component, useState ,markup} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: { type: String },
        slots: { type: Object,optional:true },
         
    };  

    setup() {
        this.state = useState({ isContent: false });
    }

    toggleContent(){
        // debugger
        this.state.isContent=!this.state.isContent
        console.log("state",this.state.isContent)
    }
}
