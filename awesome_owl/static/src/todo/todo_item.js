import { Component, xml } from "@odoo/owl";


export class TodoItem extends Component {
    static props = { 
        id: Number,
        description: String,
        isCompleted: Boolean,
        toggleTodo: Function,
        removeTodo: Function
    }
    
    static template = xml`
        <div class="border d-flex gap-1 align-items-center">   
            <input type="checkbox" t-att-checked="props.isCompleted" t-on-change="() => props.toggleTodo(props.id)" />
            <div 
                class=""
                t-att-class="{
                    'text-muted text-decoration-line-through':  props.isCompleted,
                }"
            >
                <span>
                    <t t-esc="props.id" />.
                    <t t-esc="props.description" />
                </span>
            </div>

            <span class="fa fa-remove text-danger" t-on-click="() => props.removeTodo(props.id)"/>
        </div>
    `
}
