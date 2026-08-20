import { Component, xml } from "@odoo/owl";

import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static props = { list: Array, toggleTodo: Function, removeTodo: Function }

    static template = xml`
        <div class="border">
            <t t-foreach="props.list" t-as="t" t-key="t.id">
                <TodoItem 
                    id="t.id"
                    description="t.description"
                    isCompleted="t.isCompleted"
                    toggleTodo.bind="props.toggleTodo"
                    removeTodo.bind="props.removeTodo"
                />  
            </t>
        </div>
    `

    static components = { TodoItem }
}
