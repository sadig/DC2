DC2.Pages.Admin.Backends.Environments.Index=function() {
  new DC2.Widgets.ButtonGroup.Index('#btngrp_backend_environments');
  new DC2.Widgets.DataList('#list_backend_environments_index');
};

$(document).ready(function() {
  new DC2.Pages.Admin.Backends.Environments.Index();
});

