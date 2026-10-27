import { Component, markup, useState, xml } from "@odoo/owl";

export class Counter extends Component {
  static template = "awesome_owl.playground";

  setup() {
    this.state = useState({ value: 0 });
  }

  changeValue() {
    const change = this.props.type === "add" ? 1 : -1;
    this.state.value += change;
    this.props.onChange(change);
  }

  static props = {
    label: { type: String },
    content: { type: String },
    type: {
      type: String,
      validate: (value) => value === "add" || value === "sub",
    },
    onChange: { type: Function },
  };
}

export class Playground extends Component {
  setup() {
    this.firstContent = markup('<span class="text-primary">First </span>');
    this.secondContent = markup('<strong class="text-success">Second </strong>');
    this.state = useState({ sum: 0 });
  }

  onChange(change) {
    this.state.sum += change;
  }

  static template = xml`
    <div class="position-relative p-3 d-flex flex-column align-items-center justify-content-center vh-100 gap-3">
      <a class="position-absolute top-0 end-0 m-1" style="font-size: 0.65rem;" href="/awesome_owl?page=todo">
        Todo List
      </a>
      <Counter
        label="'Counter : '"
        content="firstContent"
        type="'add'"
        onChange.bind="onChange"
      />
      <Counter
        label="'Retnuoc : '"
        content="secondContent"
        type="'sub'"
        onChange.bind="onChange"
      />
      <hr class="w-100" />
      <h1>Total : <t t-esc="state.sum" /></h1>
    </div>
  `;

  static components = { Counter };
}
