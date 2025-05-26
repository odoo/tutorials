import { Component, useState, xml } from "@odoo/owl"
import { useAutofocus } from "../utils"


export class TodoInput extends Component {

    static template = xml`
        <div>
            <input 
                placeholder="Add a todo"
                t-ref="todoInput"
                t-model="state.inputValue"
                t-on-keyup="ev => this.check(ev)"
            />
            <span t-esc="props.inputValue" />
        </div>
    `

    setup() {
        this.state = useState({inputValue : ""})
        this.inputRef = useAutofocus("todoInput")
    }

    static props = {
        addTodoItem: {type: Function},
    }

    _updateInputValue(event) {
        this.state.inputValue = event.target.value;
    }

    check(ev) {
        if (ev.keyCode === 13 && this.state.inputValue != ""){ // 13 is the code for enter key in input 
            this.props.addTodoItem(this.state.inputValue)
            this.state.inputValue = ""
        }
    }
}