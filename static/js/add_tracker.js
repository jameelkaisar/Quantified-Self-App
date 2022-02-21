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
    controller.style.display = "none";
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
        controller.style.display = "block";
        addOption();
    }
    else if (selected == "Integer" || selected == "Decimal") {
        const label = document.createElement("label");
        const unit = document.createElement("input");

        label.for = "t_unit";
        label.innerText = "Unit:";
        unit.type = "text";
        unit.id = "t_unit";
        unit.name = "t_unit";
        unit.maxLength = "16";
        unit.required = true;
        t_unit_block.appendChild(label);
        t_unit_block.appendChild(unit);

        controller.style.display = "none";
    }
    else {
        controller.style.display = "none";
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
    const para = document.createElement("p");
    const label = document.createElement("label");
    const option = document.createElement("input");

    label.for = "option[" + parseInt(to_total.value) + "]";
    label.innerText = "Option " + (parseInt(to_total.value)+1) + ":";
    option.type = "text";
    option.id = "t_option[" + parseInt(to_total.value) + "]";
    option.name = "t_option[" + parseInt(to_total.value) + "]";
    option.maxLength = "64";
    option.required = true;
    para.appendChild(label);
    para.appendChild(option);

    to_total.value = parseInt(to_total.value) + 1;
    changeOptionsButton(to_total);
    t_options.appendChild(para);
}


function remOption() {
    const to_total = document.getElementById("to_total");
    const t_options = document.getElementById("t_options");

    to_total.value = parseInt(to_total.value) - 1;
    changeOptionsButton(to_total);
    t_options.removeChild(t_options.lastChild);
}
