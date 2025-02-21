/** @odoo-module **/

import { Component , markup , useState} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card  } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components= { Counter , Card , TodoList };

    setup(){
        this.str1 = "<div class='text-primary'>Some Content</div>";
        this.str2 = markup("<div class='text-primary'>Not some Content</div>");
        this.state = useState({
            sum: 0
        })
    }
    incrementSum(){
        this.state.sum+=1;
    }
}
