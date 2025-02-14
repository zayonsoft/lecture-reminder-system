function activateNavBtn() {
    let navBtn = document.querySelector("button.nav-btn");
    let pageCover = document.querySelector("div.page-cover");
    navBtn.addEventListener("click", () => {
        if (pageCover.classList.contains("sidebar-closed")) {
            openNav();
        }
        else {
            closeNav();
        }
    });

}


function openNav() {
    let pageCover = document.querySelector("div.page-cover");
    pageCover.classList.remove("sidebar-closed");
    pageCover.classList.add("sidebar-opened");

}

function closeNav() {
    let pageCover = document.querySelector("div.page-cover");
    pageCover.classList.remove("sidebar-opened");
    pageCover.classList.add("sidebar-closed");
}

function activateCloseAsideOnClick() {
    let aside = document.querySelector("aside");
    aside.addEventListener("click", (e) => {
        if (e.target.classList.contains("close-on-click")) {
            closeNav();
        }

    });
}


document.addEventListener("DOMContentLoaded", () => {
    activateNavBtn();
    activateCloseAsideOnClick();
});