/** @odoo-module **/

import {registry} from '@web/core/registry';
import { Component, useState, onWillStart, useRef } from '@odoo/owl';
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
        this.searchInput = useRef("search-input")

        onWillStart(async ()=>{
            await this.getAllTasks();
        })

    }

    async getAllTasks(){
        this.state.taskList = await this.orm.searchRead(this.model, [], ['name', 'color', 'completed'])
    }

    addTask(){
        this.resetForm();
    }

    editTask(task){
        this.state.task = {...task};
        this.state.isEdit = true;
        this.state.activeId = task.id;

    }

    async saveTask(){
        if(!this.state.isEdit){
            await this.orm.create(this.model, [this.state.task]);
        }else{
            await this.orm.write(this.model, [this.state.activeId], this.state.task );
        }

        await this.getAllTasks();
    }

    async deleteTask(task){
        await this.orm.unlink(this.model,[task.id]);
        await this.getAllTasks()
    }

    async searchTask(){
        const text = this.searchInput.el.value
        this.state.taskList = await this.orm.searchRead(this.model, [['name', 'ilike', text]], ['name', 'color', 'completed'])
    }

    async toggleTask(e, task){
        await this.orm.write(this.model, [task.id], {completed: e.target.checked})
        await this.getAllTasks()
    }

    async toggleColor(e, task){
        await this.orm.write(this.model, [task.id], {color: e.target.value})
        await this.getAllTasks()
    }

    resetForm(){
        this.state.task = {name:"", color:"#ff0000", completed:false};
        this.state.isEdit = false;
        this.state.activeId = false;
    }
}
registry.category('actions').add('owl.action_todo_list_js', OwlTodoList)
