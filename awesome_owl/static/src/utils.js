import { useRef, onMounted } from "@odoo/owl";
export const useAutofocus = (ref) => {
    const inputRef = useRef(ref);
    onMounted(() => {
        inputRef.el.focus();
    });
};
