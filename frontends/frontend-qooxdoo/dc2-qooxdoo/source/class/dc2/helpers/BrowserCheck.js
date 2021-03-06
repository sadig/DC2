/* *******************************************************************************

   (DC)² - DataCenter Deployment Control
   Copyright (C) 2010, 2011  Stephan Adig <sh@sourcecode.de>
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
********************************************************************************* */

qx.Class.define("dc2.helpers.BrowserCheck",
    {
      statics: {
        RPCUrl:function(devel) {
          if (devel == true) {
            return "http://dc2/RPC";
          } else { 
            return  localStorage.getItem("DC2-RPCUrl");
          }
        },
        HTTPUsername:function() {
          var a=localStorage.getItem("DC2-Username");
          if (a != null) {
            return a;
          }
        },
        HTTPPassword:function() {
          var a=localStorage.getItem("DC2-Password");
          if (a != null) {
            return a;
          }
        }
      }
    });
