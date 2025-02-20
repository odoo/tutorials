import { Component, useState} from "@odoo/owl";

export class Card extends Component{      
       static template = "awesome_owl.Card"
       static props = {

              title : {
                  type : String,
                  required : true
              },
              slots: {
                type: Object,
                shape: {
                    default: true
                },
       }
    }
    setup() {
        this.state = useState({ isOpen: false });
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }
}
