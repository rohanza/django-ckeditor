CKEDITOR.plugins.add("codemirror",{requires:["sourcearea"],init:function(a){var d=this.path;a.on("mode",function(){if(a.mode=="source"){var c=a.textarea.getParent().$.clientHeight+"px",e=CodeMirror.fromTextArea(a.textarea.$,{stylesheet:d+"css/colors.css",path:d+"js/",parserfile:"parsemixed.js",passDelay:300,passTime:35,continuousScanning:1E3,undoDepth:1,height:a.config.height||c,textWrapping:false,lineNumbers:false,enterMode:"flat"});a.on("beforeCommandExec",function(b){b.removeListener();a.textarea.setValue(e.getCode());
a.fire("dataReady")});CKEDITOR.plugins.mirrorSnapshotCmd={exec:function(b){if(b.mode=="source"){b.textarea.setValue(e.getCode());b.fire("dataReady")}}};a.addCommand("mirrorSnapshot",CKEDITOR.plugins.mirrorSnapshotCmd)}});a.on("instanceReady",function(c){c.removeListener();a.mode=="wysiwyg"&&a.getData().indexOf("<?php")!==-1&&a.execCommand("source")})}});