import { Component, useState, xml } from "@odoo/owl";

export class TodoItem extends Component {
    static props = {
        todo: { type: Object, shape: { id: Number, description: String, isCompleted: Boolean } },
        toggleState: {type: Function},
        removeTodo: {type: Function}
    };

    static template = xml`
        <p t-att-class="{'text-muted text-decoration-line-through': props.todo.isCompleted}">
            <input type="checkbox" t-att="['checked', props.todo.isCompleted]" t-on-change="changeState"/>
            <t t-esc='props.todo.id'/>. 
            <t t-esc='props.todo.description'/>
            <span class="fa fa-remove" t-on-click="removeTodo"/>
        </p>
    `;

    changeState(ev){
        this.props.toggleState(this.props.todo.id, ev.target.checked);
        this.props.todo.isCompleted = ev.target.checked;
    }

    removeTodo(ev){
        this.props.removeTodo(this.props.todo.id);
    }
}
