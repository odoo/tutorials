import { useRef, onMounted, onPatched } from "@odoo/owl";

export function useAutofocus(ref) {
    const inputRef = useRef(ref);
    onMounted(() => {
        if (inputRef.el) {
            inputRef.el.focus();
        }
    });
    onPatched(() => {
        if (inputRef.el) {
            inputRef.el.focus();
        }
    });
    return inputRef;
}
