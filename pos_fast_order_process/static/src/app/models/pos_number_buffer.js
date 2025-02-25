/** @odoo-module **/

import { numberBufferService } from "@point_of_sale/app/utils/number_buffer_service";
import { patch } from "@web/core/utils/patch";

const originalStart = numberBufferService.start;

patch(numberBufferService, {
    start(env, deps) {
        const numberBufferInstance = originalStart.call(this, env, deps);
        if (typeof numberBufferInstance?.switchComponentStack !== 'function') {
            numberBufferInstance.switchComponentStack = function(component_name) {
                if (!this.bufferHolderStack || !Array.isArray(this.bufferHolderStack)) {
                    return;
                };

                const indexComponent = this.bufferHolderStack.findIndex(
                    (stack) => stack.component?.constructor?.name === component_name
                );
                if (indexComponent === -1) {
                    return;
                };

                const componentEntry = this.bufferHolderStack.splice(indexComponent, 1)[0];
                if (componentEntry) {
                    this.bufferHolderStack.push(componentEntry);
                };
                if (typeof this._setUp === 'function') {
                    this._setUp();
                };
            };
        };
        return numberBufferInstance;
    },
});
