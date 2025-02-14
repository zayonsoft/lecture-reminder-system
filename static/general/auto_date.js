function activateInsertDate() {
    let yearDeveloped = '2025';
    let currentYear = new Date().getFullYear().toString();
    let dateSpan = document.querySelectorAll(".insert-date");
    let dateString = yearDeveloped;
    if (currentYear != yearDeveloped) {
        dateString = `${yearDeveloped} - ${currentYear}`;
    }
    dateSpan.forEach((span) => {
        span.innerHTML = dateString;
    });
}

document.addEventListener("DOMContentLoaded", function () {
    activateInsertDate();
});