const toasts = document.getElementsByClassName("toast");

for (let i=0; i<toasts.length; i++) {
    new bootstrap.Toast(toasts[i]).show();
}
