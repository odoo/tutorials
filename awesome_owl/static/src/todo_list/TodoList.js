import { Component, useState} from "@odoo/owl";
import { TodoItem } from "./TodoItem";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };

    setup() {
        this.todos = useState([ ]);
        this.state = useState({
            next_id: 1,
        })
    }

    onInputKeyup(ev) {
        if (ev.key === "Enter") {
            const value = ev.target.value.trim();
            if (value) {
                const next_id = this.state.next_id++;
                this.todos.push(
                    {
                        id: next_id,
                        description: value,
                        isCompleted: false
                    }
                )
                ev.target.value = "";
            }
        }
    }

}
