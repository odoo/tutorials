/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { scanBarcode } from "@web/core/barcode/barcode_dialog";
import { rpc } from "@web/core/network/rpc";

export class KioskMainScreen extends Component {
  static template = "time_tracking_kiosk.KioskMainScreen";

  setup() {
    this.state = useState({
      employeeId: "",
      employee: null,
      currentProject: null,
      currentTask: null,
      isTimerRunning: false,
      timerStartTime: null,
      timesheetId: null,
      screen: "scan",
      elapsedTime: "00:00:00",
      timerInterval: null,
    });
    this.orm = useService("orm");
    this.notification = useService("notification");
    this.scanBarcode = () => scanBarcode(this.env, this.facingMode);
  }

  async openMobileScanner() {
    let error = null;
    let barcode = null;
    try {
      barcode = await this.scanBarcode();
    } catch (err) {
      error = err.message;
    }

    if (barcode) {
      this.onBarcodeScanned(barcode);
      if ("vibrate" in window.navigator) {
        window.navigator.vibrate(100);
      }
    } else {
      this.notification.add(error || _t("Please, Scan again!"), {
        type: "warning",
      });
    }
  }

  onBarcodeScanned(barcode) {
    this.state.employeeId = barcode;
    this.onScanBadge();
  }

  async onScanBadge() {
    if (!this.state.employeeId) {
      this.notification.add("Please scan or enter an employee ID", {
        type: "warning",
      });
      return;
    }

    try {
      const employees = await this.orm.call(
        "hr.employee",
        "search_read",
        [[["barcode", "=", this.state.employeeId]]],
        { limit: 1 }
      );
      if (employees.length) {
        const employee = employees[0];
        const tasks = await this.orm.call(
          "project.task",
          "search_read",
          [[["user_ids", "in", [employee.user_id[0]]]]],
          {
            fields: ["id", "name", "project_id", "effective_hours", "stage_id"],
          }
        );
        if (tasks.length == 0) {
          this.notification.add(
            `Employee ${employee.name} has no tasks currently assigned. Please assign tasks to enable time tracking.`,
            {
              type: "warning",
            }
          );
          this.state.screen = "scan";
          return;
        }
        const stages = await this.orm.call(
          "project.task.type",
          "search_read",
          [[["id", "in", tasks.map((task) => task.stage_id[0])]]],
          { fields: ["id", "fold"] }
        );

        const stageMap = stages.reduce((map, stage) => {
          map[stage.id] = stage.fold;
          return map;
        }, {});

        const projectsMap = {};

        tasks.forEach((task) => {
          if (stageMap[task.stage_id[0]]) return;
          const projectId = task.project_id[0];
          const projectName = task.project_id[1];
          if (!projectsMap[projectId]) {
            projectsMap[projectId] = {
              id: projectId,
              name: projectName,
              tasks: [],
            };
          }

          projectsMap[projectId].tasks.push({
            id: task.id,
            name: task.name,
            effective_hours: task.effective_hours,
          });
        });

        this.state.employee = {
          ...employee,
          assigned_projects: Object.values(projectsMap),
        };

        const activeTimesheet = await this.orm.call(
          "account.analytic.line",
          "search_read",
          [
            [
              ["employee_id", "=", employee.id],
              ["timer_active", "=", true],
            ],
          ],
          {
            limit: 1,
            fields: ["id", "timer_start_time", "project_id", "task_id"],
          }
        );

        if (activeTimesheet.length) {
          this.state.isTimerRunning = true;
          this.state.timerStartTime = new Date(
            activeTimesheet[0].timer_start_time
          );

          this.state.timerStartTime = new Date(
            this.state.timerStartTime.getTime() -
              this.state.timerStartTime.getTimezoneOffset() * 60000
          );
          this.state.timesheetId = activeTimesheet[0].id;

          if (activeTimesheet[0].project_id && activeTimesheet[0].task_id) {
            const projectId = activeTimesheet[0].project_id[0];
            const projectName = activeTimesheet[0].project_id[1];

            this.state.currentProject =
              this.state.employee.assigned_projects.find(
                (proj) => proj.id === projectId
              );

            if (!this.state.currentProject) {
              this.state.currentProject = {
                id: projectId,
                name: projectName,
                tasks: [],
              };
            }

            const taskId = activeTimesheet[0].task_id[0];
            const taskName = activeTimesheet[0].task_id[1];

            this.state.currentTask = this.state.currentProject.tasks.find(
              (task) => task.id === taskId
            );

            if (!this.state.currentTask) {
              this.state.currentTask = {
                id: taskId,
                name: taskName,
              };

              if (
                !this.state.currentProject.tasks.some(
                  (task) => task.id === taskId
                )
              ) {
                this.state.currentProject.tasks.push(this.state.currentTask);
              }
            }
          }

          this.state.screen = "timer";
          this.startElapsedTimeUpdater();
        } else {
          this.state.screen = "projects";
        }

        this.notification.add(`Employee Found: ${employee.name}`, {
          type: "success",
        });
      } else {
        this.notification.add("Employee not found!", { type: "danger" });
      }
    } catch (error) {
      this.notification.add("An error occurred while fetching employee data.", {
        type: "danger",
      });
    }
  }

  onProjectChange(event) {
    const projectId = Number(event.target.value);

    this.state.currentProject =
      this.state.employee.assigned_projects.find(
        (proj) => proj.id === projectId
      ) || null;

    this.state.currentTask = null;
  }

  onTaskChange(event) {
    const taskId = Number(event.target.value);

    this.state.currentTask =
      this.state.currentProject?.tasks.find((task) => task.id === taskId) ||
      null;
  }

  backToMainScreen() {
    if (this.state.timerInterval) {
      clearInterval(this.state.timerInterval);
      this.state.timerInterval = null;
    }

    this.state.employeeId = "";
    this.state.employee = null;
    this.state.currentProject = null;
    this.state.currentTask = null;
    this.state.timerStartTime = null;
    this.state.screen = "scan";
  }

  async startTimer() {
    const { currentProject, currentTask, employee } = this.state;

    if (!currentProject || !currentTask) {
        this.notification.add("Please select a project and task first!", {
            type: "warning",
        });
        return;
    }

    try {
        const timesheetData = await rpc("/timesheet/create", {
            project_id: currentProject.id,
            task_id: currentTask.id,
            employee_id: employee.id,
        });

        if (timesheetData.id) {
            this.state.isTimerRunning = true;
            this.state.timerStartTime = new Date();
            this.state.timesheetId = timesheetData.id;
            this.state.screen = "timer";
            this.startElapsedTimeUpdater();
            this.notification.add("Timer started successfully!", { type: "success" });
        } else {
            this.notification.add("Failed to start timer.", { type: "danger" });
        }
    } catch (error) {
        this.notification.add("Error starting timer.", { type: "danger" });
    }
}

  async stopTimer() {
    if (!this.state.isTimerRunning || !this.state.timesheetId) {
      this.notification.add("No active timer found.", { type: "warning" });
      return;
    }

    try {
      const response = await rpc("/timesheet/stop", {
        timesheet_id: this.state.timesheetId,
      });

      if (response.error) {
        this.notification.add(response.error, { type: "danger" });
        return;
      }

      if (response.id) {
        this.notification.add(
          `Timesheet stopped. Worked ${
            Math.round(response.unit_amount * 60) / 100
          } hours`,
          { type: "success" }
        );
      } else {
        this.notification.add("Failed to stop timer.", { type: "danger" });
      }
    } catch (error) {
      this.notification.add("Error stopping timer.", { type: "danger" });
    }

    if (this.state.timerInterval) {
      clearInterval(this.state.timerInterval);
      this.state.timerInterval = null;
    }

    this.state.isTimerRunning = false;
    this.state.timerStartTime = null;
    this.state.timesheetId = null;
    this.state.screen = "scan";
  }

  startElapsedTimeUpdater() {
    if (this.state.timerInterval) {
      clearInterval(this.state.timerInterval);
    }

    this.updateElapsedTime();

    this.state.timerInterval = setInterval(() => {
      this.updateElapsedTime();
    }, 1000);
  }

  updateElapsedTime() {
    if (!this.state.timerStartTime) return;

    const now = new Date();
    const elapsedMilliseconds = now - this.state.timerStartTime;
    const totalSeconds = Math.floor(elapsedMilliseconds / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    this.state.elapsedTime = `${hours.toString().padStart(2, "0")}:${minutes
      .toString()
      .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  }

  formatTime(date) {
    if (!date) return "00:00:00";

    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");
    const seconds = date.getSeconds().toString().padStart(2, "0");

    return `${hours}:${minutes}:${seconds}`;
  }
}

registry.category("actions").add("time_tracking_kiosk_main", KioskMainScreen);


