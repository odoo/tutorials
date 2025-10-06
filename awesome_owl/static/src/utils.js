import { onMounted, useRef } from '@odoo/owl';

export const useAutoFocus = (inputFieldRefName) => {
    const addTaskInputRef = useRef(inputFieldRefName);
    onMounted(() => {
        addTaskInputRef.el.focus();
    });
}