import {Component, useRef} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props ={
        id: Number,
        description: String,
        active: Boolean,
        onToggle: Function,
    };

    get activeCheck(){
        let classes = "p-2";
        if(!this.props.active){
            classes += " text-muted text-decoration-line-through";
        }
        return classes;
    }


    boxClicked(){
        this.props.onToggle()
    }
    
}
