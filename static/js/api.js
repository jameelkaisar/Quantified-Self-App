function copyToken() {
    const user_token = document.getElementById("user_token");
    const user_token_copy = document.getElementById("user_token_copy");

    const tooltip = bootstrap.Tooltip.getInstance(user_token_copy);
    tooltip.dispose();

    user_token_copy.setAttribute("title", "Copied!");
    new bootstrap.Tooltip(document.getElementById("user_token_copy")).show();;

    // navigator clipboard api needs a secure context (https)
    if (navigator.clipboard && window.isSecureContext) {
        // navigator clipboard api method
        return navigator.clipboard.writeText(user_token.value);
    } else {
        // text area method
        let textArea = document.createElement("textarea");
        textArea.value = user_token.value;
        // make the textarea out of viewport
        textArea.style.position = "absolute";
        textArea.style.opacity = 0;
        document.body.appendChild(textArea);
        textArea.select();
        return new Promise((res, rej) => {
            document.execCommand("copy") ? res() : rej();
            textArea.remove();
        });
    }
}


function copyFinish() {
    const user_token_copy = document.getElementById("user_token_copy");

    const tooltip = bootstrap.Tooltip.getInstance(user_token_copy);
    tooltip.dispose();

    user_token_copy.setAttribute("title", "Click to copy");
    new bootstrap.Tooltip(document.getElementById("user_token_copy"));
}


function enableTooltip() {
    new bootstrap.Tooltip(document.getElementById("user_token_copy"));
}


enableTooltip();
