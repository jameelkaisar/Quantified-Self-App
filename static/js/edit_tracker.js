function changeOptionsButton(to_total) {
    const button = document.getElementById("t_options_rem");

    if (to_total.value > 0) {
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
    option.setAttribute("placeholder", "New Option " + (parseInt(to_total.value)+1));
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


function remOptionExist(object) {
    const parent = object.parentElement;
    const grandparent = parent.parentElement;
    parent.remove();
    if (grandparent.children.length == 0) {
        grandparent.innerHTML = "All Existing Nodes Deleted";
    }
}


function enableTooltips() {
    const to_total_exist = document.getElementById("to_total_exist");

    for (let i=1; i<=to_total_exist.value; i++) {
        new bootstrap.Tooltip(document.getElementById("t_option_exist_del[" + i + "]"));
    }
}


enableTooltips();
