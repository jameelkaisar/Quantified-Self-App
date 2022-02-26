function resetForm() {
    const controller = document.getElementById("t_options_control");
    const to_total = document.getElementById("to_total");
    const t_options = document.getElementById("t_options");
    const t_unit_block = document.getElementById("t_unit_block");

    to_total.value = 0;
    while (t_unit_block.firstChild) {
        t_unit_block.removeChild(t_unit_block.firstChild);
    }
    while (t_options.firstChild) {
        t_options.removeChild(t_options.firstChild);
    }
    controller.classList.add("d-none");

    changeOptionsButton(to_total);
}


function setTypeOptions(select) {
    const controller = document.getElementById("t_options_control");
    const to_total = document.getElementById("to_total");
    const t_options = document.getElementById("t_options");
    const t_unit_block = document.getElementById("t_unit_block");
    const selected = select.options[select.selectedIndex].text;

    to_total.value = 0;
    while (t_unit_block.firstChild) {
        t_unit_block.removeChild(t_unit_block.firstChild);
    }
    while (t_options.firstChild) {
        t_options.removeChild(t_options.firstChild);
    }

    if (selected == "Single Select" || selected == "Multi Select") {
        controller.classList.remove("d-none");
        addOption();
    }
    else if (selected == "Integer" || selected == "Decimal") {
        const block = document.createElement("div");
        const unit = document.createElement("input");

        block.classList.add("mb-3");
        unit.type = "text";
        unit.classList.add("form-control");
        unit.id = "t_unit";
        unit.name = "t_unit";
        unit.maxLength = "16";
        unit.setAttribute("placeholder", "Unit");
        unit.required = true;
        block.appendChild(unit);
        t_unit_block.appendChild(block);

        controller.classList.add("d-none");
    }
    else {
        controller.classList.add("d-none");
    }
}


function changeOptionsButton(to_total) {
    const button = document.getElementById("t_options_rem");

    if (to_total.value > 1) {
        button.disabled = false;
    }
    else {
        button.disabled = true;
    }
}


function addOption() {
    const to_total = document.getElementById("to_total");
    const t_options = document.getElementById("t_options");
    const block = document.createElement("div");
    const option = document.createElement("input");

    block.classList.add("mb-3");
    option.type = "text";
    option.classList.add("form-control");
    option.id = "t_option[" + parseInt(to_total.value) + "]";
    option.name = "t_option[" + parseInt(to_total.value) + "]";
    option.maxLength = "64";
    option.setAttribute("placeholder", "Option " + (parseInt(to_total.value)+1));
    option.required = true;
    block.appendChild(option);

    to_total.value = parseInt(to_total.value) + 1;
    changeOptionsButton(to_total);
    t_options.appendChild(block);
}


function remOption() {
    const to_total = document.getElementById("to_total");
    const t_options = document.getElementById("t_options");

    to_total.value = parseInt(to_total.value) - 1;
    changeOptionsButton(to_total);
    t_options.removeChild(t_options.lastChild);
}
