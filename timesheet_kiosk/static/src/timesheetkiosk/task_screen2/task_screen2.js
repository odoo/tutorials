/** @odoo-module **/
import { Component } from "@odoo/owl";

export class TaskScreen2 extends Component {
    static template = "timesheet_kiosk.TaskScreen2";
    static props = ["employee", "tasks", "timertask", "timmerproject", "timerlineid", "goToStart", "stopTimer"];



    back() {
        this.props.goToStart();
    }

    get activeTask() {
        return this.props.tasks.find(t => t.id === this.props.timertask) || {};
    }

    stopTimer() {
        this.props.stopTimer(this.props.timerlineid);
    }
}
