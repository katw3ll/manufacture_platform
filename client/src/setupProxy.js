const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:8000/api",
      pathRewrite: {
        "^/api": "",
      },
      changeOrigin: true,
    })
  );
};

// module.exports = function (app) {
//   app.use(
//     "/auth",
//     createProxyMiddleware({
//       target: "http://localhost:8000/auth",
//       pathRewrite: {
//         "^/auth": "",
//       },
//       changeOrigin: true,
//     })
//   );
// };