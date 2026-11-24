// GoodBuy Foods Global: serves the static site and sends www.goodbuyfoods.com to goodbuyfoods.com,
// so search engines see one canonical site.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "www.goodbuyfoods.com") {
      url.hostname = "goodbuyfoods.com";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
