import { useRef, onMounted } from "@odoo/owl";

/**
 * Custom hook to automatically focus an element when 
 * the component is mounted.
 * @param {string} name - The t-ref name used in the XML
 */
export function useAutofocus(name) {
    const ref = useRef(name);

    onMounted(() => {
        if (ref.el) {
            ref.el.focus();
        }
    });

    return ref;
}
