
function removeSectionPreloader() {
    let sectionPreloader = document.querySelector(".section-preloader");
    sectionPreloader.style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
    removeSectionPreloader();
});

