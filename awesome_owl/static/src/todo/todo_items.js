/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class TodoItem extends Component {
  static template = xml`
        <div t-att-class="{'text-muted text-decoration-line-through': props.todo.isCompleted}" padding="5px">
            <input type="checkbox"
                style="margin:10px;"
                t-att-checked="props.todo.isCompleted"
                t-on-change="() => props.toggleState(props.todo.id)" />
            <strong  style="margin-right:5px;"><t t-esc="props.index"/>:</strong>
            <t t-esc="props.todo.description"/>
            <span class="fa fa-remove" style="color:red; margin:10px;" t-on-click="() => props.removeTodo(props.todo.id)" />
        </div>
    `;

  static props = {
    todo: {
      type: Object,
      shape: {
        id: Number,
        description: String,
        isCompleted: Boolean,
      },
      optional: false,
    },
    index : Number,
    toggleState: {
      type: Function,
      optional: false,
    },
    removeTodo: {
      type: Function,
      optional: false,
    },
  };
}
