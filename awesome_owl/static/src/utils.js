import { onMounted } from "@odoo/owl";

/**
 * Automatically focuses on the provided reference element when the component is mounted.
 *
 * @param {Object} ref - The reference object to the DOM element.
 * @returns {void}
 */
export const useAutofocus = (ref) => {
    onMounted(() => {
        if (ref?.el) {
            ref.el.focus();
        }
    });
};
