function setDateTime() {
    const tl_time = document.getElementById("tl_time");
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    tl_time.value = now.toISOString().slice(0,16);
}


setDateTime();
