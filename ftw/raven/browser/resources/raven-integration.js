if (typeof raven_config !== "undefined") {
  // From: https://gist.github.com/impressiver/5092952
  var ravenOptions = {
    // Will cause a deprecation warning, but the demise of `ignoreErrors` is still under discussion.
    // See: https://github.com/getsentry/raven-js/issues/73
    ignoreErrors: [
        // Random plugins/extensions
        'top.GLOBALS',
        // See: http://blog.errorception.com/2012/03/tale-of-unfindable-js-error.html
        'originalCreateNotification',
        'canvas.contentDocument',
        'MyApp_RemoveAllHighlights',
        'http://tt.epicplay.com',
        'Can\'t find variable: ZiteReader',
        'jigsaw is not defined',
        'ComboSearch is not defined',
        'http://loading.retry.widdit.com/',
        'atomicFindClose',
        // Facebook borked
        'fb_xd_fragment',
        // ISP "optimizing" proxy - `Cache-Control: no-transform` seems to reduce this. (thanks @acdha)
        // See http://stackoverflow.com/questions/4113268/how-to-stop-javascript-injection-from-vodafone-proxy
        'bmi_SafeAddOnload',
        'EBCallBackMessageReceived',
        // See http://toolbar.conduit.com/Developer/HtmlAndGadget/Methods/JSInjection.aspx
        'conduitPage',
        // Generic error code from errors outside the security sandbox
        // You can delete this if using raven.js > 1.0, which ignores these automatically.
        'Script error.'
    ]
  };

  /* Testing function */
  function raven_test() {
    try {
      throw "Raven JavaScript test exception";
    } catch(e) {
      Raven.captureException(e);
    }
  }

  /* Update raven config options with default config from ravenOptions: */
  for (key in ravenOptions) {
    raven_config['options'][key] = ravenOptions[key];
  }

  if (raven_config['user_context'] != undefined) {
    Raven.setUserContext(raven_config['user_context']);
    Raven.config(raven_config['dsn'], raven_config['options']);
  }
}
