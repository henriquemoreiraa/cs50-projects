document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".btn-bg");
  const mode = localStorage.getItem("mode");

  const setDarkMode = () => {
    document.body.style.background = "#1f1f1f";
    document.body.style.color = "#f5f5f5";
    document.querySelector(".btn-bg").innerHTML = "🌚";
  };

  const setLightMode = () => {
    document.body.style.background = "#fff";
    document.body.style.color = "#313131";
    document.querySelector(".btn-bg").innerHTML = "🌞";
  };

  if (mode === "dark") {
    setDarkMode();
  } else setLightMode();

  button.addEventListener("click", () => {
    const mode = localStorage.getItem("mode");

    if (mode === "dark") {
      localStorage.setItem("mode", "light");
      setLightMode();
    } else {
      localStorage.setItem("mode", "dark");
      setDarkMode();
    }
  });
});
