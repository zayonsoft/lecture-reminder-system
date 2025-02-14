function hideNavLinks() {
    let sideBar = document.querySelector(".page-content aside");
    let appName = document.querySelector(".app-name");
    appName.classList.add("small-header")
    sideBar.classList.remove("show-links");
    sideBar.classList.add("hide-links");
}

function showNavLinks() {
    let sideBar = document.querySelector(".page-content aside");
    let appName = document.querySelector(".app-name");
    appName.classList.remove("small-header")
    sideBar.classList.remove("hide-links");
    sideBar.classList.add("show-links");
}

function activeLinksControl() {
    let sideBar = document.querySelector(".page-content aside");
    let barController = document.querySelector("button.bar-controller");
    barController.addEventListener("click", () => {
        if (sideBar.classList.contains("show-links")) {
            hideNavLinks();
        }
        else if (sideBar.classList.contains("hide-links")) {
            showNavLinks();
        }
    });
}

//closes the nav when the main area of the page is clicked
function closeNavOnClick() {
    let mainContent = document.querySelector(".page-content main");
    mainContent.addEventListener("click", () => {
        hideNavLinks();
    });

}

document.addEventListener("DOMContentLoaded", () => {
    activeLinksControl();
    closeNavOnClick()
});

