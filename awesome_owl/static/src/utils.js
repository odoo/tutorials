import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(tRefName) {
    const inputRef = useRef(tRefName);
    onMounted(() => {
        if (inputRef.el) {
            inputRef.el.focus();
        }
    });
    return inputRef;
}
