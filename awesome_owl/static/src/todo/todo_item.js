import { Component, xml } from "@odoo/owl"

export class TodoItem extends Component {
    static template = xml`
        <div t-att-class="props.isCompleted ? 'text-muted text-decoration-line-through' : ''">
            <input 
                type="checkbox" 
                t-att-checked="props.isCompleted"
            />

            <t t-esc="props.id"/>. 
            <t t-esc="props.description"/>

            <span 
                class="fa fa-remove" 
                style="color: red; margin-left:4px" 
                t-on-click="() => this.props.removeTodo(props.id)"
            />
        </div>
    `

    static props = {
        id: {type: Number},
        description: {type: String},
        isCompleted:  {type: Boolean},
        toggleTodo: {type: Function},
        removeTodo: {type: Function},
    }
}