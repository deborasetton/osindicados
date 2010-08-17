/*********************** Funcoes da tela de partida ***********************/

function liftOff() { 
    window.location = '../erro/' 
}

function watchCountdown(periods) { 
    $('#monitor').text('Just ' + periods[5] + 
        ' minutes and ' + periods[6] + ' seconds to go'); 
} 

function serverTime() { 
    var time = null; 
    $.ajax({url: 'http://localhost:8000/jogo/horario/', 
        async: false, dataType: 'text', 
        success: function(text) { 
            time = new Date(text); 
        }, error: function(http, message, exc) { 
            time = new Date(); 
    }}); 
    return time; 
}

function aumentarTempo() { 
    $.ajax({url: 'http://localhost:8000/jogo/ajudaTempo/', 
        async: true, dataType: 'text', 
        error: function(http, message, exc) { 
            alert('erro');
    }}); 
    apagarUmaEstrelaDoTempo();
}

function highlightLast5(periods) { 
    if ($.countdown.periodsToSeconds(periods) == 5) { 
        $(this).addClass('highlight'); 
    } 
} 

 $(document).ready(function() {
 
	$('#timer').countdown({
      until: +30, 
      format: 'S', 
      compact: true, 
      onExpiry: liftOff, 
      onTick: highlightLast5, 
      serverSync: serverTime});
	
	valor = $('#responder_frm input[type=submit]').position().top;
	valor += 122;
	$('#timer').css('margin-top', valor + 'px');
});
 
$(window).load(function () {
	$('#loading_inicio').hide();
});
 
 function ajudaElimina() {
	$('#timer').countdown('pause');
	$('#timer').hide();
	$('#divloading').show();
    $('#replace').load("http://localhost:8000/jogo/ajudaElimina/ #alternativas", function(){
    	$('#timer').countdown('resume');
    	$('#timer').show();
    	$('#divloading').hide();
	});
    $('#linkElimina').replaceWith('<img height="32px" width="" style="border-style: none;" src="/osindicadosmedia/img/strikethroughdisabled.png" title="Voc&ecirc; j&aacute; esgotou suas ajudas de elimina&ccedil;&atilde;o para essa pergunta" alt="Voc&ecirc; j&aacute; esgotou suas ajudas de elimina&ccedil;&atilde;o para essa pergunta!">');
    apagarUmaEstrela();
}
 
 function apagarUmaEstrela() {
	 
	 imagens = $('#table-ajudas #imagensElimina img');

	 $.each(imagens,
	     function(index, imgtag) {
	           var src = ($(imgtag).attr("src") === "/osindicadosmedia/img/star.png")
	                     ? "/osindicadosmedia/img/starblack.png" 
	                     : "/osindicadosmedia/img/star.png";  
	     
	     if((src) === "/osindicadosmedia/img/starblack.png")
	     {
	          //alert(src);
	         $(imgtag).attr("src", src);
	            return false;
	     }
	    
	 });
 }
 
 function apagarUmaEstrelaDoTempo(){
	 imagens = $('#table-ajudas #imagensTempo img');
	 var achou;
	 
	 $.each(imagens,
	     function(index, imgtag) {
	           var src = ($(imgtag).attr("src") === "/osindicadosmedia/img/star.png")
	                     ? "/osindicadosmedia/img/starblack.png" 
	                     : "/osindicadosmedia/img/star.png";  
	     
	     if((src) === "/osindicadosmedia/img/starblack.png")
	     {
	          //alert(src);
	         $(imgtag).attr("src", src);
	         return false;
	     }
	 });
	 
	 $('#linkTempo').replaceWith('<img height="32px" width="" style="border-style: none;" src="/osindicadosmedia/img/ampulhetadisabled.jpg" title="Voc&ecirc; j&aacute; esgotou suas ajudas de tempo para essa pergunta!" alt="Voc&ecirc; j&aacute; esgotou suas ajudas de tempo para essa pergunta!">');
 }
 
 function verificarSelecao() {
	alts = $('#form-pergunta :radio');
	pass = false;
	$.each(alts , function(alt, index) {
		if(index.checked) pass = true;
	}); 
	if(!pass){
		alert('Selecione uma altertnativa!');
		return false;
	}
	$('#loading_inicio').show();
	return true;
}

 
 
 