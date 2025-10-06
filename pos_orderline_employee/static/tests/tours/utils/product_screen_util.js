export function clickEmployeeButton() {
    return [
        {
            content: "Ensure an order line is selected",
            trigger: ".order-container .orderline ",
        },
        {
            content: "click employee button",
            trigger: ".product-screen .set-employee",
            run: "click",
        },
    ];
}

export function clickEmployee(name = "") {
    return {
        content: `Click employee '${name}' from employee list screen`,
        trigger: `.modal .employee-list tbody tr:has(.employee-name div:contains("${name}"))`,
        run: "click",
    };
}

export function checkContactValues(name, mobile = "", email = "") {
    const steps = [
        {
            content: `Check employee "${name}" from employee list screen`,
            trigger: `.employee-list tr:has(.employee-name:contains("${name}"))`,
        },
    ];

    if (mobile) {
        steps.push({
            content: `Check mobile number "${mobile}" for employee "${name}"`,
            trigger: `.employee-list tr:has(.employee-name:contains("${name}")) .employee-line-phone:contains("${mobile}")`,
        });
    }

    if (email) {
        steps.push({
            content: `Check email address "${email}" for employee "${name}"`,
            trigger: `.employee-list tr:has(.employee-name:contains("${name}")) .employee-line-email .email-field:contains("${email}")`,
        });
    }

    return steps;
}

export function searchEmployeeValue(val) {
    return [
        {
            isActive: ["mobile"],
            content: `Click search field`,
            trigger: `.modal-dialog .input-group input`,
            run: `click`,
        },
        {
            content: `Search customer with "${val}"`,
            trigger: `.modal-dialog .input-group input`,
            run: `edit ${val}`,
        },
    ];
}
