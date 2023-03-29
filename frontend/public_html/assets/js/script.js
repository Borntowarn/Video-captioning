
function checkAddress(){

    var switch_btn = document.getElementById('switch_btn').checked;
    //var path_video = document.getElementById('path_to_video').src;


    // запрос обработанного видео
    if(switch_btn){
        $.ajax({
            type:"GET",
            url:"http://projectvoid.play.ai:8080/api/get_video",
            dataType:"json",
            data: {
                'film_id': 4,
                'only_updated': 1
            },
            beforeSend: function() {
                document.getElementById('animation').style.display = 'block';
                document.getElementById('video_body').style.display = 'none';
            },
            complete: function(data) {

                console.log(data.responseText);

                if(data.responseText != 'Фильм еще не обработан'){
                    document.getElementById('animation').style.display = 'none';
                    document.getElementById('video_body').style.display = 'block';
                }

                document.getElementById('path_to_video').src = 'http://projectvoid.play.ai:8080/api/get_video?film_id=4&only_updated=1';
                console.log(document.getElementById('path_to_video').src);
                var player = document.getElementById('player');
                player.load();
            }
        });
    }else{  // запрос стандартного видео
        $.ajax({
            type:"GET",
            url:"http://projectvoid.play.ai:8080/api/get_video",
            dataType:"json",
            data: {
                'film_id': 4,
                'only_updated': 0
            },
            beforeSend: function() {
                document.getElementById('animation').style.display = 'block';
                document.getElementById('video_body').style.display = 'none';
            },
            complete: function() {
                console.log(123);
                document.getElementById('animation').style.display = 'none';
                document.getElementById('video_body').style.display = 'block';

                document.getElementById('path_to_video').src = 'http://projectvoid.play.ai:8080/api/get_video?film_id=4&only_updated=0';
                console.log(document.getElementById('path_to_video').src);
                var player = document.getElementById('player');
                player.load();
            }
        });
    }






}