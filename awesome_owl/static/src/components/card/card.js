import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String, 
        slots: {
            type: Object,
            shape: {
                default: true
            }
        }
    };

    setup() {
        this.state = useState({renderContent: true});
    }

    toggleContent(){
        this.state.renderContent = !this.state.renderContent;
    }

}