import { Component  } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title : String ,text: String,
        obj : Object,
        handledone : Function,  
    }

    
    
    setup() {
        
        
    }
    
    
    handle_the_done(param){
        debugger;
        if (this.props.handledone) {
            this.props.handledone(param);
        }
        else{
            alert("the handle done func is not given");
        }
    }

}
