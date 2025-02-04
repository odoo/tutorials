import { Component, useState} from "@odoo/owl"

export class Card extends Component{
    static template = "awesome_owl.card";
    setup() {
        this.state = useState({
            isOpen: false
        });
    }

}
