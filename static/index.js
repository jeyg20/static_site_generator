const navBar = document.querySelector("#nav-bar");
const navItems = navBar.querySelectorAll(".nav-item");

navItems.forEach(function (item) {
  item.addEventListener("click", function () {
    const currentActive = navBar.querySelector(".active");

    if (currentActive) {
      currentActive.classList.remove("active");
    }

    this.classList.add("active");
  });
});
