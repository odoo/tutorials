/** @odoo-module **/

import {registry} from '@web/core/registry';
import { Component, useState, onWillStart } from '@odoo/owl';
import { useService } from '@web/core/utils/hooks';

class OwlTodoList extends Component {
    static template= 'owl.TodoList';
    setup() {
        this.state = useState({
            task:{name:"", color:"#ff0000", completed:false},
            taskList:[],
            isEdit: false,
            activeId: false
        });
        this.orm = useService('orm');
        this.model = "todo.list";

        onWillStart(async ()=>{
            await this.getAllTasks();
        })

    }

    async getAllTasks(){
        this.state.taskList = await this.orm.searchRead(this.model, [], ['name', 'color', 'completed'])
    }

    addTask(){

    }

    editTask(){

    }

    async saveTask(){
        await this.orm.create(this.model, [{
            name: this.state.task.name,
            color: this.state.task.color,
            completed: this.state.task.completed
        }]);
    }
}
registry.category('actions').add('owl.action_todo_list_js', OwlTodoList)
