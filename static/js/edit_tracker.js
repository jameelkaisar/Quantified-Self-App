function resetForm() {
    const controller = document.getElementById("t_options_control");
    const to_total = document.getElementById("to_total");
    const t_options = document.getElementById("t_options");
    const t_unit_block = document.getElementById("t_unit_block");

    to_total.value = Math.min(to_original, to_total.value);
    to_original = Math.min(to_original, to_total.value);
    while (t_options.childElementCount > to_total.value) {
        t_options.removeChild(t_options.lastChild);
    }

    changeOptionsButton(to_total);
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

    label.setAttribute("for", "option[" + parseInt(to_total.value) + "]");
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


var to_original = document.getElementById("to_total").value;
