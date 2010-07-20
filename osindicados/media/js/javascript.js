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
        async: false, dataType: 'text', 
        success: function(text) { 
            alert('ok'); 
        }, error: function(http, message, exc) { 
            alert('erro');
    }}); 
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
 });
 
 function ajudaElimina() {
    $('#alternativas').load("http://localhost:8000/jogo/ajudaElimina/")
 }
 
 
 