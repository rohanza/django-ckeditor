var stringStream=function(i){function j(){for(;c==b.length;){e+=b;b="";c=0;try{b=i.next()}catch(a){if(a!=StopIteration)throw a;else return false}}return true}var b="",c=0,e="";return{peek:function(){if(!j())return null;return b.charAt(c)},next:function(){if(!j())if(e.length>0)throw"End of stringstream reached without emptying buffer ('"+e+"').";else throw StopIteration;return b.charAt(c++)},get:function(){var a=e;e="";if(c>0){a+=b.slice(0,c);b=b.slice(c);c=0}return a},push:function(a){b=b.slice(0,
c)+a+b.slice(c)},lookAhead:function(a,d,f,n){function g(k){return n?k.toLowerCase():k}a=g(a);var h=false,l=e,o=c;for(f&&this.nextWhileMatches(/[\s\u00a0]/);;){f=c+a.length;var m=b.length-c;if(f<=b.length){h=a==g(b.slice(c,f));c=f;break}else if(a.slice(0,m)==g(b.slice(c))){e+=b;b="";try{b=i.next()}catch(p){break}c=0;a=a.slice(m)}else break}if(!(h&&d)){b=e.slice(l.length)+b;c=o;e=l}return h},more:function(){return this.peek()!==null},applies:function(a){var d=this.peek();return d!==null&&a(d)},nextWhile:function(a){for(var d;(d=
this.peek())!==null&&a(d);)this.next()},matches:function(a){var d=this.peek();return d!==null&&a.test(d)},nextWhileMatches:function(a){for(var d;(d=this.peek())!==null&&a.test(d);)this.next()},equals:function(a){return a===this.peek()},endOfLine:function(){var a=this.peek();return a==null||a=="\n"}}};