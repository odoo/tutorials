import { Component, xml } from "@odoo/owl";

export class TodoItem extends Component {
  static template = xml`<li t-att-class="{'text-muted text-decoration-line-through': props.todo.isCompleted}">
	  <input type="checkbox" t-on-change="_onChecked" t-att-checked="props.todo.isCompleted" />
    <span t-out="props.todo.id"/> - <span t-out="props.todo.description"/>
    <button class="btn btn-danger" t-on-click="_onDelete"><span class="fa fa-remove"/></button>
  </li>`;

  static props = {
    todo: {
      type: Object,
      shape: {
        id: Number,
        description: String,
        isCompleted: Boolean,
      },
    },
    toggle: {
      type: Function,
    },
    delete: {
      type: Function,
    },
  };

  _onChecked(event) {
    this.props.toggle(this.props.todo.id, event.target.checked);
  }
  _onDelete() {
    this.props.delete(this.props.todo.id);
  }
}
