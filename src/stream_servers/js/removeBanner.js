function removeBanner() {
  const divs = $("div");
  
  divs.filter(index => {
    const div = divs[index]
    return !div.className && $(div).css("z-index") == 9999
  })[0].remove();

}

removeBanner();
