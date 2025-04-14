/** @odoo-module **/

import { Component } from '@odoo/owl';
import {registry} from '@web/core/registry';
import {useState} from '@odoo/owl';

class OwlTodoList extends Component {
    static template= 'owl.TodoList';
    setup() {
        this.state = useState({value:45});
        
    }
}
registry.category('actions').add('owl.action_todo_list_js', OwlTodoList)