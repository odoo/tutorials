import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);

        if (this.props.resModel === "library.borrow") {
            this.notificationService = useService("notification");
        }
    },

    async beforeExecuteActionButton(clickParams) {
        if (this.props.resModel === "library.borrow") {
            this._prevStateBeforeAction = this.model.root.data.state;
        }
        return super.beforeExecuteActionButton(...arguments);
    },

    async afterExecuteActionButton(clickParams) {
        if (this.props.resModel === "library.borrow") {
            const currentState = this.model.root.data.state;
            const prevState = this._prevStateBeforeAction;

            if (prevState !== "returned" && currentState === "returned") {
                this.notificationService.add("Book returned! Congratulations! 🎉", {
                    type: "success",
                    sticky: false,
                });
            }
        }
        return super.afterExecuteActionButton(...arguments);
    },
});
