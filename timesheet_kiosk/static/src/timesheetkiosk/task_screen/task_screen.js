/** @odoo-module **/
import { Component, useState } from "@odoo/owl";

export class TaskScreen extends Component {
    static template = "timesheet_kiosk.TaskScreen";
    static props = ["employee", "tasks", "projects", "goToStart", "startTimer"];

    setup() {
        this.state = useState({ projectId: null, taskId: null });
    }

    get filteredTasks() {
        if (!this.state.projectId) return this.props.tasks;
        return this.props.tasks.filter(t => t.project_id[0] === this.state.projectId);
    }

    onProjectChange(ev) {
        this.state.projectId = ev.target.value ? parseInt(ev.target.value) : null;
        this.state.taskId = null;
    }

    onTaskChange(ev) {
        const taskId = ev.target.value ? parseInt(ev.target.value) : null;
        this.state.taskId = taskId;
        if (taskId) {
            const task = this.props.tasks.find(t => t.id === taskId);
            this.state.projectId = task.project_id[0];
        }
    }

    back() { 
        this.props.goToStart(); 
    }
    startTimer() { 
        this.props.startTimer(this.state.taskId); 
    }
}
