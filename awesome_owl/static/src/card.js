import { Component , useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static components = { }

    setup(){
        this.showCardContent = useState({value:true});
    }

    toggleCardContent(){
        this.showCardContent.value = !this.showCardContent.value;
    }
}
