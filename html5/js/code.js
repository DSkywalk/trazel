/*!
 * Trazel JavaScript Library v1
 * https://github.com/DSkywalk/trazel/
 *
 * Copyright 2014 - David Colmenero (D_Skywalk)
 * Released under GPL v3 license
 * http://david.dantoine.org/proyecto/25/
 *
 * Date: 2014-2-4
 */
 
 if (window.addEventListener){ //IE Fix
	window.addEventListener("load", eventWindowLoaded, false);
} else if (window.attachEvent){
	window.attachEvent('load', eventWindowLoaded);
}
function eventWindowLoaded() { canvasApp(); }
var Debugger = function () { };
Debugger.log = function (message) { try { console.log(message); } catch (exception) { return; } }
function canvasSupport() {
  var elem = document.createElement('canvas');
  return !!(elem.getContext && elem.getContext('2d') && typeof(Object.keys) == 'function' && typeof(opera) == 'undefined');
}

function canvasApp(){
	if (!canvasSupport()) { alert("NO SOPORTADO!"); return; }
	
    var theCanvas = document.getElementById("canvasMap");
	var style = theCanvas.getAttribute('style') || '';
	var context = theCanvas.getContext("2d");
	context.font="10px Serif";
	
    Debugger.log('Canvas INIT!');
	
	theCanvas.addEventListener("mousedown",eventMouseUp, false);

	var background = new Image();
	background.addEventListener('load', eventImgLoaded , false);
	background.src = "img/bg2.png"; //bg-test.png

	var tile = new Image();
	tile.addEventListener('load', eventImgLoaded , false);
	tile.src = "img/tilechars2.png";

    var loadedImg = 0;
    var amountToLoad = 2;

	Debugger.log('Canvas Loading!');
	
	/**
	 *  Draw Code
	 */
	
    // Clean Functions
	function cleanFullBackground() {
		context.save();
		context.setTransform(1,0,0,1,0,0); // reset
		//draw using fixed size
		// calc new scale (mantener aspect ratio)
		context.drawImage(background, 0, 0);
		context.restore();
	    context.fillStyle = "white";
		context.fillRect(8, 120, 100, 16);
	}
	
	
	var CharInfo = {sX: 0, Index: 0};
	var CurrentChar = -1;
	var LineX = 12;
	var LineY = 12;
	var WaitLoop = false;
	var TextScroll = false;
	var gOpacity = 1;
	
    /*  65 = A - 97 = a
     * 243 = ó - 
     *   A B C D E F G H I J K L M N O P
     *   Q R S T U V W é Y Z a b c d e f
     *   g h i j k l m n o p q r s t u v
     *   ó x y z 0 1 2 3 4 5 6 7 8 9 ! ?
     *   - . , … > ( ) ñ ú á @@@ " ↑↓ ←
     *   → í ♥   ♥    ♥    ♥    < A B X Y |
     *   ¡ ¿         …
     */
     
	// Draw Functions
	function objectDraw(Index, pX, pY, opacity) {
		var sourceX = Math.floor(Index % 16) * 16;
		var sourceY = Math.floor(Index / 16) * 32;

		context.save();
		context.setTransform(1,0,0,1,0,0); // reset
		
		context.translate(pX, pY);
		
		context.globalAlpha = opacity;
		
		//Debugger.log(sourceX +" "+ sourceY + " " + Index + " f:" + " p:" +pX);
		context.drawImage(tile, sourceX, sourceY, 
							16, 32, 0, 0, 16, 32);
		
		context.restore();
		
	}
	
	function scrollText() {
	    Debugger.log("SCROLL!");
		context.save();
		context.setTransform(1,0,0,1,0,0); // reset
		context.translate(12, 12);
	    context.globalAlpha = 1;
	    context.drawImage(theCanvas, 12, 44, 376, 64, 0, 0, 376, 64);
	    context.fillStyle = "RED";
	    context.fillRect(0, 64, 343, 32);
	    context.fillStyle = "BLACK";
	    context.fillRect(0, 64, 340, 32);
		context.restore();
	}
	
	function waitText() {
   	    context.fillStyle = "RED";
        context.fillText("WAITING...",12,132);	
	}
	
	
	/**
	 * MAIN
	 */
	 
	function decodeChar(chr) {
	    code = chr.charCodeAt(0);
        CharInfo.sX = 12;
        CharInfo.Index = 0;

	    if(code >= 65 && code <= 90)
	        CharInfo.Index = (code - 65);
	    if(code >= 97 && code <= 122)
	        CharInfo.Index = (code - (97 - 26));
	    if(code >= 48 && code <= 58)
	        CharInfo.Index = (code + 4);
	    
        switch(code){
            case 32: CharInfo.Index = 89; CharInfo.sX = 8; break; // espacio
            case 95: CharInfo.Index = 89; CharInfo.sX = 16; break; // espacio2
            case 43: CharInfo.Index = 89; CharInfo.sX = (8*3); break; // espacio {88}
            case 42: CharInfo.Index = 89; CharInfo.sX = (8*4); break; // espacio {89}
            
            case 33: CharInfo.Index = 62; CharInfo.sX = 6; break; // !
            case 34: CharInfo.Index = 76; CharInfo.sX = 16; break; // "
            case 40: CharInfo.Index = 69; break; // (
            case 41: CharInfo.Index = 70; break; // )
            case 44: CharInfo.Index = 66; CharInfo.sX = 8; break; //,
            case 46: CharInfo.Index = 65; CharInfo.sX = 8; break; //.
            case 183: CharInfo.Index = 67; break; //...d

            case 62: CharInfo.Index = 68; CharInfo.sX = 16; break; //selector |>
            case 63: CharInfo.Index = 63; CharInfo.sX = 14; break; // ?
            case 65: break; // A
            case 73: CharInfo.sX = 6; break; // I
            case 84: case 86: case 87: case 89: case 77: CharInfo.sX = 14; break; //MTVWY
            case 106: CharInfo.sX = 10; break; //j
            case 109: case 118: case 120: case 121: CharInfo.sX = 14; break; //mv
            case 105: CharInfo.sX = 6; break; //i
            case 108: CharInfo.sX = 6; break; //l
            case 114: CharInfo.sX = 10; break; //r
            
            case 191: CharInfo.Index = 97; CharInfo.sX = 16; break; //¿
            case 194: CharInfo.Index = 74; CharInfo.sX = 16; break; // Link1
            case 195: CharInfo.Index = 75; CharInfo.sX = 16; break; // Link2
            case 192: CharInfo.Index = 77; CharInfo.sX = 16; break; // F. Arriba
            case 200: CharInfo.Index = 78; CharInfo.sX = 16; break; // F. Abajo
            case 204: CharInfo.Index = 79; CharInfo.sX = 16; break; // F. Izq
            case 210: CharInfo.Index = 80; CharInfo.sX = 16; break; // F. Der
            case 212: CharInfo.Index = 82; CharInfo.sX = 16; break; // Cor. Izq Medio
            case 214: CharInfo.Index = 83; CharInfo.sX = 16; break; // Cor. Der vacío
            case 211: CharInfo.Index = 84; CharInfo.sX = 16; break; // Cor. Izq Lleno
            case 213: CharInfo.Index = 85; CharInfo.sX = 16; break; // Cor. Der Lleno
            case 216: CharInfo.Index = 86; CharInfo.sX = 16; break; // Cor. Der Medio
            case 208: CharInfo.Index = 87; CharInfo.sX = 16; break; // Cor. Izq Completo
            case 223: CharInfo.Index = 88; CharInfo.sX = 16; break; // Cor. Der Completo
            case 161: CharInfo.Index = 96; CharInfo.sX = 16; break; //¡
            case 193: CharInfo.Index = 91; CharInfo.sX = 16; break; // [A]
            case 201: CharInfo.Index = 92; CharInfo.sX = 16; break; // [B]
            case 205: CharInfo.Index = 94; CharInfo.sX = 16; break; // [Y]
            case 218: CharInfo.Index = 93; CharInfo.sX = 16; break; // [X]
            
            case 225: CharInfo.Index = 73; break; //á
            case 233: CharInfo.Index = 23; CharInfo.sX = 12; break; //é
            case 237: CharInfo.Index = 81; CharInfo.sX = 6;  break; //í
            case 243: CharInfo.Index = 48; CharInfo.sX = 12; break; //ó
            case 250: CharInfo.Index = 72; break; //ú
            case 241: CharInfo.Index = 71; break; //ñ
            
            // simbolos hylianos
            case 219: CharInfo.Index = 22; CharInfo.sX = 16; break;  // Hylia - 1 (la W)
            case 220: CharInfo.Index = 64; break;  // Hylia - 2 (el -)
            case 217: CharInfo.Index = 90; CharInfo.sX = 16; break; // Hylia - 3 ( la <| )

            // especiales            
            case 35: LineY += 32; LineX = 12; CharInfo.Index = 89; CharInfo.sX = 0; break; //ln
            case 126: WaitLoop = true; CharInfo.sX = 0; LineX = 12; break; //wait
            case 172: LineX = 12; TextScroll = true; CharInfo.sX = 0; break; //scroll
            default:
                if(!CharInfo.Index)
                    Debugger.log("Code: " + code + " not found?!");
                break;
        
        }
	}
	 
    function drawScreen() {
        var text = $("#ttext").val();

        if(CurrentChar == -1){
            LineX = 12;
            LineY = 12;
            CurrentChar = 0;
            WaitLoop = false;
            TextScroll = false;
            cleanFullBackground();
        }

        if(text == '')
            return;
        
        text = text.replace("[1]","#")
                   .replace("[2]","#")
                   .replace("[3]","#")
                   .replace(/\.\.\./g, "·")
                   .replace(/\[60\]/g, "¡")
                   .replace(/\[61\]/g, "¿")
                   .replace(/\[S1\]/g, "Û")
                   .replace(/\[S2\]/g, "Ü")
                   .replace(/\[S3\]/g, "Ù")
                   .replace("[A]", "Á")
                   .replace("[B]", "É")
                   .replace("[Y]", "Í")
                   .replace("[X]", "Ú")
                   .replace("|>", ">")
                   .replace(/\{4A\}/gi, "Â")
                   .replace(/\{4B\}/gi, "Ã")
                   .replace(/\{4D\}/gi, "À")
                   .replace(/\{4E\}/gi, "È")
                   .replace(/\{4F\}/gi, "Ì")
                   .replace(/\{50\}/gi, "Ò")
                   .replace(/\{52\}/gi, "Ô")
                   .replace(/\{53\}/gi, "Ö")
                   .replace(/\{54\}/gi, "Ó")
                   .replace(/\{55\}/gi, "Õ")
                   .replace(/\{56\}/gi, "Ø")
                   .replace(/\{57\}/gi, "Ð")
                   .replace(/\{58\}/gi, "ß")
                   .replace(/\{88\}/gi, "*")
                   .replace(/\{89\}/gi, "+")
                   .replace(/\[Waitkey\]/gi, "~")
                   .replace(/\[Scroll\]/gi, "¬")
                   .replace(/\<Espacio 2\>/gi, "_")
                   .replace(/\[Espacio 2\]/gi, "_")
                   .replace(/\[43\]|\[66\]/gi, "·")
                     .replace(/\[Choose\]/gi, "")
                    .replace("{END}", "")
                    .replace("[END]", "")
                    .replace(/\[|\]/g,"");
        
        for ( ; CurrentChar < text.length; CurrentChar++){
            decodeChar(text.charAt(CurrentChar));
            if(WaitLoop){ waitText(); WaitLoop = CurrentChar + 1; break;}
            if(TextScroll){ scrollText(); TextScroll = false; }

            Debugger.log(text.charAt(CurrentChar) + " code (" + text.charAt(CurrentChar).charCodeAt(0) + ") decode (" + CharInfo.Index + ") sX(" + CharInfo.sX + ") lY("+LineY+")" );
            objectDraw(CharInfo.Index, LineX , LineY, gOpacity);
            LineX+= CharInfo.sX;
        }
        
        if(CurrentChar == text.length)
            CurrentChar = -1;
    }
	
	
	/**
	 *  Events
	 */

    $("#ttext").on('keyup paste', function() {
        CurrentChar = -1;
        drawScreen();
    })
	
	function eventImgLoaded() {
		loadedImg ++;
		if(loadedImg == amountToLoad){
			startUp();
		}
	}

    function eventMouseUp(event) {
		event.preventDefault();
		if(WaitLoop){
    		Debugger.log("CLICK!");
		    CurrentChar = WaitLoop;
			WaitLoop = false;
    	    context.fillStyle = "white";
			context.fillRect(8, 120, 100, 16);
			drawScreen();
	    }
	}
		
	function startUp(){
		Debugger.log("Finished Loading");
        drawScreen();
        
        // i dont need real time render...
        // better on change => refresh :D
        
		//bNeedFullRedraw = true;
		//setInterval(drawScreen, 24 );
	}
	
	
	
}
