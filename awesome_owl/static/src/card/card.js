import { useState, Component, xml, markup } from "@odoo/owl"

export class Card extends Component {
  static template = 'awesome_owl.card'

  static props = {
    title: String,
    slots: {
      type: Object,
      shape: {
        default: Object
      },
      optional: true
    }
  };

  setup() {
    this.html = "<div class='text-primary'>some content</div>"
    this.state = useState({
      title: "",
      content: "",
      toggle: false
    })
    this.value1 = markup(this.html)
    this.handleToggle = this.handleToggle.bind(this)
  }

  handleToggle() {
    this.state.toggle = !this.state.toggle
  }

}
