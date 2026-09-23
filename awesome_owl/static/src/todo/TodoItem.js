import {Component, xml} from "@odoo/owl"

export class TodoItem extends Component {
    static template = xml`
    <input type="checkbox" t-att-checked="props.todo.isCompleted"
            t-on-change="onChange"
            style="margin-right: 1em"
    />
    <span t-att-class="props.todo.isCompleted? 'text-muted  text-decoration-line-through': ''" >
    <t t-esc="props.todo.id" />.  <t t-esc="props.todo.description" />
    </span>
    <span style="margin-left: 0.5em" class="fa fa-remove" t-on-click="remove"/>
    `

    onChange(event) {
        console.log('on change');
        this.props.toggleState(this.props.todo.id)
        console.log(event);
    }

    remove(event) {
        this.props.removeTodo(this.props.todo.id);
    }

    static props = {
        todo: true,
        toggleState: true,
        removeTodo: true
    }
}
