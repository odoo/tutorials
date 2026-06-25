import { Component, useState , markup} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList };
    static props = {};
    setup(){
        this.html =  markup("<p>This is a playground to test Owl components.</p>");
        this.state = useState({
            count1:0,
            count2:0
        });
    }
    updateCount1 (val) {
        this.state.count1 = val;
    }
    updateCount2 (val) {
        this.state.count2 = val;
    }
}
