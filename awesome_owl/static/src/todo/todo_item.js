/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Todoitem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
    item: {type: Object
    },
    delete: {type: Function
    }
    }
    check = () =>{
        this.props.item.isCompleted = !this.props.item.isCompleted
    }

}
