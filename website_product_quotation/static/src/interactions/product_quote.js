import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";

export class ProductQuote extends Interaction {
    static selector = ".o_product_quote";

    dynamicContent = {
        ".o_next": {
            "t-on-click": () => {
                this.rotateToIndex(this.currentIndex + 1);
            },
        },
        ".o_prev": {
            "t-on-click": () => {
                this.rotateToIndex(this.currentIndex - 1);
            },
        },
        ".o_extra_image": {
            "t-on-click": (event) => {
                this.imageUpdater(event);
            },
        },
        ".o_copy_link": {
            "t-on-click": (event) => {
                this.copyShareLink(event);
            },
        },
        ".o_get_quote_btn": {
            "t-on-click": () => {
                this.isShown = false;
                this.updateFormDetails();
            },
        },
        ".o_form_section": {
            "t-att-class": () => ({ "d-none": this.isShown }),
            "t-on-click": (ev) => {
                const form_container =
                    this.el.querySelector(".o_form_container");
                if (form_container && !form_container.contains(ev.target)) {
                    this.isShown = true;
                }
            },
        },
        // To make Form Invisible as soon as submit button is clicked
        // ".o_form_submit": {
        //     "t-on-click": () => {
        //         this.isShown = true;
        //         this.updateFormDetails();
        //     },
        // },
    };

    setup() {
        this.ul = this.el.querySelector("#circle--rotate");
        this.lis = this.ul.querySelectorAll("li");
        this.totalItems = this.lis.length;
        this.step = 360 / this.totalItems;
        this.animates = this.el.querySelectorAll(".animate");
        this.currentIndex = 0;
        this.angle = 0;
        this.isShown = true;
        this.positionListItems();
    }

    positionListItems() {
        const center = {
            x: this.ul.clientWidth / 2,
            y: this.ul.clientHeight / 2,
        };
        const radius =
            (Math.min(this.ul.clientWidth, this.ul.clientHeight) / 2) * 0.82;
        const emBase = parseFloat(getComputedStyle(this.ul).fontSize);

        this.lis.forEach((li, index) => {
            const itemAngle =
                (index / this.totalItems) * 2 * Math.PI - Math.PI / 2;
            const x = (center.x + radius * Math.cos(itemAngle)) / emBase;
            const y = (center.y + radius * Math.sin(itemAngle)) / emBase;

            li.style.left = `${x}em`;
            li.style.top = `${y}em`;

            const degrees = (itemAngle * 180) / Math.PI + 90;
            li.style.transform = `translate(-50%, -50%) rotate(${degrees}deg)`;

            const icon = li.querySelector(".icon");
            if (icon) {
                icon.style.transform = `rotate(0deg)`;
            }

            li.addEventListener("click", () => this.rotateToIndex(index));
        });
    }

    rotateToIndex(index) {
        if (index < 0) index = this.totalItems - 1;
        if (index >= this.totalItems) index = 0;

        this.currentIndex = index;
        this.angle = -index * this.step;
        this.ul.style.transform = `rotate(${this.angle}deg)`;
        this.lis.forEach((li, i) => li.classList.toggle("active", i === index));
        this.animates.forEach((animate, i) => {
            if (i === index) {
                animate.classList.add("active");
            } else {
                animate.classList.remove("active");
            }
        });
    }

    imageUpdater(event) {
        const element = event.target;
        let parentContainer = element.closest(".product-category-slider");

        let mainImage = parentContainer.querySelector(".img-fluid");
        let mainImageName = parentContainer.querySelector(".extra-img-name");
        let activeImages = parentContainer.querySelectorAll(".thumb-item");

        if (mainImage) {
            mainImage.src = element.getAttribute("src");
        }

        if (mainImageName) {
            mainImageName.textContent = element.getAttribute("data-name") || "";
        }

        activeImages.forEach((img) => img.classList.remove("activeimg"));
        element.classList.add("activeimg");
    }

    copyShareLink(event) {
        event.preventDefault();
        const element = event.target;
        const link = element.href;
        navigator.clipboard.writeText(link);
        alert("Copied the text: \n" + link);
    }

    updateFormDetails() {
        this.active_animate_wrapper = this.el.querySelectorAll(".active")[1];
        this.product = this.active_animate_wrapper.getAttribute("data-key");
        this.product = JSON.parse(this.product.replace(/'/g, '"'));

        this.product_name =
            this.active_animate_wrapper.querySelector(
                ".o_product_name"
            ).textContent;
        this.el.querySelector("#product_name").value = this.product.name || "";

        this.populateOptions("Size", this.product.size || []);
        this.populateOptions("Fabric", this.product.fabric || []);
        this.populateOptions("Color", this.product.color || []);
        this.populateOptions("Print", this.product.print || []);
    }

    populateOptions(fieldName, options) {
        const formContainer = this.el.querySelector("form .row");
        if (!formContainer) return;

        const submitButtonContainer = formContainer.querySelector(
            ".s_website_form_submit"
        );

        if (!options.length) {
            const existingBlock = formContainer.querySelector(
                `.s_website_form_field[data-name='${fieldName}']`
            );
            if (existingBlock) existingBlock.remove();
            return;
        }

        let fieldBlock = formContainer.querySelector(
            `.s_website_form_field[data-name='${fieldName}']`
        );

        if (!fieldBlock) {
            fieldBlock = document.createElement("div");
            fieldBlock.className =
                "s_website_form_field mb-3 col-12 s_website_form_custom col-lg-11";
            fieldBlock.setAttribute("data-name", fieldName);
            fieldBlock.setAttribute("data-type", "one2many");

            fieldBlock.innerHTML = `
                <label class="s_website_form_label">
                    <span class="s_website_form_label_content">${fieldName}</span>
                </label>
                <div class="row s_col_no_resize s_col_no_bgcolor s_website_form_multiple" data-name="${fieldName}" data-display="horizontal">
                </div>
            `;

            formContainer.insertBefore(fieldBlock, submitButtonContainer);
        }

        const container = fieldBlock.querySelector(`.s_website_form_multiple`);
        container.innerHTML = "";

        const fragment = document.createDocumentFragment();
        options.forEach((option, index) => {
            const newCheckbox = document.createElement("div");
            newCheckbox.className = "checkbox col-12 col-lg-4 col-md-6";
            newCheckbox.innerHTML = `
                <div class="form-check">
                    <input type="checkbox" class="s_website_form_input form-check-input"
                        id="${fieldName.toLowerCase()}_option_${index}"
                        name="${fieldName}"
                        value="${option}" />
                    <label class="form-check-label s_website_form_check_label"
                        for="${fieldName.toLowerCase()}_option_${index}">
                        ${option}
                    </label>
                </div>
            `;
            fragment.appendChild(newCheckbox);
        });

        container.appendChild(fragment);
    }
}

registry
    .category("public.interactions")
    .add("website_product_quotation.product_quote", ProductQuote);
