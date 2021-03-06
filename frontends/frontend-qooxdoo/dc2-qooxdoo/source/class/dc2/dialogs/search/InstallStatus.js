/*
    (DC)² - DataCenter Deployment Control
    Copyright (C) 2010, 2011, 2012, 2013  Stephan Adig <sh@sourcecode.de>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
*/

qx.Class.define("dc2.dialogs.search.InstallStatus",
{
  extend: dc2.widgets.DialogWidget,
  construct:function() {
    this.base(arguments);
  },
  members: {
    _edit_hostname:null,
    _edit_status:null,
    _createLayout:function() {
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,10);
      layout.setColumnFlex(1,1);
      comp.setLayout(layout);
      this._edit_hostname=new qx.ui.form.TextField();
      this._edit_status=new qx.ui.form.SelectBox();
      comp.add(new qx.ui.basic.Label("Hostname"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Status"),{row:1,column:0});
      comp.add(this._edit_hostname,{row:0,column:1});
      comp.add(this._edit_status,{row:1,column:1});
      this._edit_status.add(new qx.ui.form.ListItem("Any",null,"any"));
      this._edit_status.add(new qx.ui.form.ListItem("Localboot",null,"localboot"));
      this._edit_status.add(new qx.ui.form.ListItem("Deploy",null,"deploy"));
      return(comp);
    },
    _getData:function() {
      var data={};
      if (this._edit_hostname.getValue() != null && this._edit_hostname.getValue() != "") {
        data["hostname"]=this._edit_hostname.getValue();
      }
      if (this._edit_status.getSelection()[0].getModel()!="any") {
        data["status"]=this._edit_status.getSelection()[0].getModel();
      }
      return(data);
    }
  }
});
