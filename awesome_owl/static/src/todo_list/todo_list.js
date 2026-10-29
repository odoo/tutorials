import { Component, useProps, t } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"; 
    
    static components = { TodoItem }

    props = useProps ({
        todos: t.array()
    })
}