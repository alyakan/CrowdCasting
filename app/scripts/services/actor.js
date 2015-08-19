app.service('actorService', function() {
 this.actorData;

  this.actor = function() {
        return this.actorData;
  };

  this.setActor = function(actor) {
        this.actorData = actor;
  };

  this.getUrl = function() {
        return this.actorData.url;
  };
  this.SetUrl = function(url) {
      this.actorData.url = url;
  };
});