<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <title>Pink Cats</title>

    <link rel="stylesheet" href="assets/css/style.css">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    <link href="assets/img/image_2023-02-18_19-43-53.png" rel="icon">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">



</head>
<body>

<div class="header">
    <div class="header-body">
        <a href="/" class="logo">KION</a>
        <div class="header-right">
            <a class="active" href="#home">Главная</a>
            <a href="#contact">Телеканалы</a>
            <a href="#about">Фильмы</a>
            <a href="#about">Сериалы</a>
        </div>
    </div>
</div>









<div class="film_preview">

    <div class="film_preview_head">

        <div class="film_preview_title">
            Белль и Себастьян: Приключения продолжаются (2015)
        </div>


        <div class="special_block">
            <div class="special_block_left">
                <div class="special_block_title">
                    Версия для слабовидящих
                </div>
                <button onclick="playSound('sound');" class="question_btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-question" viewBox="0 0 16 16">
                        <path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286zm1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94z"/>
                    </svg>
                </button>
            </div>
<!--            <div class="button b2" id="button-11" onchange="checkAddress()">-->
<!--                <input type="checkbox" class="checkbox" id="switch_btn">-->
<!--                <div class="knobs">-->
<!--                    <span></span>-->
<!--                </div>-->
<!--                <div class="layer"></div>-->
<!--            </div>-->


            <div class="switch_bloc">
                <label class="checkbox-green">
                    <input type="checkbox" id="switch_btn" onchange="checkAddress()">
                    <span class="checkbox-green-switch" data-label-on="Вкл." data-label-off="Выкл."></span>
                </label>
            </div>


        </div>

    </div>


    <div class="animation" id="animation" style="display: none">

        <div class="center">
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
        </div>


    </div>



    <main id="video_body">
        <div id="container">
            <video
                    controls
                    crossorigin
                    playsinline
                    data-poster="https://cdn.plyr.io/static/demo/View_From_A_Blue_Moon_Trailer-HD.jpg"
                    id="player"
                    style="width: 65%;"
            >
                <!-- Video files -->
                <!--                        http://pinkcats.my.to:8080/api/get_video?film_id=2&only_updated=0-->
                <source
                        src="http://pinkcats.my.to:8080/api/get_video?film_id=4&only_updated=0"
                        type="video/mp4"
                        size="1080"
                        id="path_to_video"
                />

            </video>
        </div>

        <ul>
            <li class="plyr__cite plyr__cite--video" hidden>
                <small>
                    <svg class="icon">
                        <title>HTML5</title>
                        <path
                                d="M14.738.326C14.548.118 14.28 0 14 0H2c-.28 0-.55.118-.738.326S.98.81 1.004 1.09l1 11c.03.317.208.603.48.767l5 3c.16.095.338.143.516.143s.356-.048.515-.143l5-3c.273-.164.452-.45.48-.767l1-11c.026-.28-.067-.557-.257-.764zM12 4H6v2h6v5.72l-4 1.334-4-1.333V9h2v1.28l2 .666 2-.667V8H4V2h8v2z"
                        ></path>
                    </svg>

                </small>
            </li>
            <li class="plyr__cite plyr__cite--audio" hidden>
                <small>
                    <svg class="icon" title="HTML5">
                        <title>HTML5</title>
                        <path
                                d="M14.738.326C14.548.118 14.28 0 14 0H2c-.28 0-.55.118-.738.326S.98.81 1.004 1.09l1 11c.03.317.208.603.48.767l5 3c.16.095.338.143.516.143s.356-.048.515-.143l5-3c.273-.164.452-.45.48-.767l1-11c.026-.28-.067-.557-.257-.764zM12 4H6v2h6v5.72l-4 1.334-4-1.333V9h2v1.28l2 .666 2-.667V8H4V2h8v2z"
                        ></path>
                    </svg>

                </small>
            </li>
            <li class="plyr__cite plyr__cite--youtube" hidden>
                <small>
                    <a href="https://www.youtube.com/watch?v=bTqVqk7FSmY" target="_blank">View From A Blue Moon</a>
                    on&nbsp;
                    <span class="color--youtube">
            <svg class="icon" role="presentation">
              <title>YouTube</title>
              <path
                      d="M15.8,4.8c-0.2-1.3-0.8-2.2-2.2-2.4C11.4,2,8,2,8,2S4.6,2,2.4,2.4C1,2.6,0.3,3.5,0.2,4.8C0,6.1,0,8,0,8
                               s0,1.9,0.2,3.2c0.2,1.3,0.8,2.2,2.2,2.4C4.6,14,8,14,8,14s3.4,0,5.6-0.4c1.4-0.3,2-1.1,2.2-2.4C16,9.9,16,8,16,8S16,6.1,15.8,4.8z
                                M6,11V5l5,3L6,11z"
              ></path></svg
            >YouTube
          </span>
                </small>
            </li>
            <li class="plyr__cite plyr__cite--vimeo" hidden>
                <small>
                    <a href="https://vimeo.com/40648169" target="_blank">Toob “Wavaphon” Music Video</a>
                    on&nbsp;
                    <span class="color--vimeo">
            <svg class="icon" role="presentation">
              <title>Vimeo</title>
              <path
                      d="M16,4.3c-0.1,1.6-1.2,3.7-3.3,6.4c-2.2,2.8-4,4.2-5.5,4.2c-0.9,0-1.7-0.9-2.4-2.6C4,9.9,3.4,5,2,5
                           C1.9,5,1.5,5.3,0.8,5.8L0,4.8c0.8-0.7,3.5-3.4,4.7-3.5C5.9,1.2,6.7,2,7,3.8c0.3,2,0.8,6.1,1.8,6.1c0.9,0,2.5-3.4,2.6-4
                           c0.1-0.9-0.3-1.9-2.3-1.1c0.8-2.6,2.3-3.8,4.5-3.8C15.3,1.1,16.1,2.2,16,4.3z"
              ></path></svg
            >Vimeo
          </span>
                </small>
            </li>
        </ul>
    </main>


</div>








<div class="film_description">
    <div class="film_description-body">
        <div class="film_description-title">
            Описание
        </div>
        <div class="film_description-text">
            Продолжение приключений мальчика Себастьяна и пиренейской горной собаки Белль.
            В небольшой французский городок Сен-Мартан в горах на границе со Швейцарией вернулась мирная размеренная жизнь,
            но не вернулась Анжелина. Однажды в городок приходит страшная весть: самолёт,
            на котором Анжелина возвращалась домой, потерпел крушение где-то в альпийских лесах. Никто, кроме Себастьяна,
            не верит, что девушка могла спастись. Верные друзья Белль и Себастьян отправляются на поиски Анжелины.
            Им предстоит пройти через множество испытаний и узнать тайну, которая изменит их жизнь навсегда.
        </div>
    </div>
</div>

<div class="actors">
    <div class="actors_body">
        <div class="actors_title">
            Актёры и съёмочная группа
        </div>
        <div class="actors_text">

            <div class="actor">
                <span class="circle-image">
                    <img src="assets/img/1_1.jpg" alt="">
                </span>
                <div class="actors_name">
                    Феликс<br>Боссюэ
                </div>
            </div>


            <div class="actor">
                <span class="circle-image">
                    <img src="assets/img/1_2.jpg" alt="">
                </span>
                <div class="actors_name">
                    Чеки<br>Карио
                </div>
            </div>
            <div class="actor">
                <span class="circle-image">
                    <img src="assets/img/1_3.jpeg" alt="">
                </span>
                <div class="actors_name">
                    Тьери<br>Новик
                </div>
            </div>
            <div class="actor">
                <span class="circle-image">
                    <img src="assets/img/1_4.jpg" alt="">
                </span>
                <div class="actors_name">
                    Марго<br>Шателье
                </div>
            </div>
            <div class="actor">
                <span class="circle-image">
                    <img src="assets/img/1_5.jpg" alt="">
                </span>
                <div class="actors_name">
                    Талан<br>Блондо
                </div>
            </div>
            <div class="actor">
                <span class="circle-image">
                    <img src="assets/img/1_6.jpg" alt="">
                </span>
                <div class="actors_name">
                    Люди<br>Бекен
                </div>
            </div>
            <div class="actor">
                <span class="circle-image">
                    <img src="assets/img/1_7.jpg" alt="">
                </span>
                <div class="actors_name">
                    Джеймс<br>Гандольфини
                </div>
            </div>

        </div>
    </div>
</div>


<div class="recommendation">
    <div class="recommendation_body">
        <div class="recommendation_title">
            Смотрите также
        </div>
        <div class="recommendation_text">

            <div class="recommendation_film">
                <span class="recommendation_circle-image">
                    <img src="assets/img/p_1.webp" alt="">
                </span>
                <div class="recommendation_name">
                    Белль и Себастьян (2013)<br>.
                </div>
            </div>
            <div class="recommendation_film">
                <span class="recommendation_circle-image">
                    <img src="assets/img/p_2.webp" alt="">
                </span>
                <div class="recommendation_name">
                    Белль и Себастьян:<br> Друзья навек (2017)
                </div>
            </div>
            <div class="recommendation_film">
                <span class="recommendation_circle-image">
                    <img src="assets/img/p_3.webp" alt="">
                </span>
                <div class="recommendation_name">
                    Белль и Себастьян:<br>  Новое поколение (2022)
                </div>
            </div>
            <div class="recommendation_film">
                <span class="recommendation_circle-image">
                    <img src="assets/img/6146129876.jpg" alt="">
                </span>
                <div class="recommendation_name">
                    Клан<br> сопрано
                </div>
            </div>
            <div class="recommendation_film">
                <span class="recommendation_circle-image">
                    <img src="assets/img/p_4.webp" alt="">
                </span>
                <div class="recommendation_name">
                    Иван Васильевич меняет<br> профессию (1973)
                </div>
            </div>
            <div class="recommendation_film">
                <span class="recommendation_circle-image">
                    <img src="assets/img/p_5.webp" alt="">
                </span>
                <div class="recommendation_name">
                    А зори здесь<br> тихие
                </div>
            </div>


        </div>
    </div>
</div>





<div id="footer" class="footer">
    <div class="main-footer widgets-dark typo-light">
        <div class="container">
            <div class="row">

                <div class="col-xs-12 col-sm-6">
                    <div class="widget no-box">
                        <h5 class="widget-title">Разделы<span></span></h5>
                        <ul class="thumbnail-widget">
                            <li>
                                <div class="thumb-content"><a href="#.">Главная</a></div>
                            </li>
                            <li>
                                <div class="thumb-content"><a href="#.">Телеканалы</a></div>
                            </li>
                            <li>
                                <div class="thumb-content"><a href="#.">Фильмы</a></div>
                            </li>
                            <li>
                                <div class="thumb-content"><a href="#.">Сериалы</a></div>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="col-xs-12 col-sm-6">
                    <div class="widget no-box">
                        <h5 class="widget-title">Помощь<span></span></h5>
                        <ul class="thumbnail-widget">
                            <li>
                                <div class="thumb-content"><a href="#.">Справка</a></div>
                            </li>
                            <li>
                                <div class="thumb-content"><a href="#.">Обратная связь</a></div>
                            </li>
                            <li>
                                <div class="thumb-content"><a href="#.">Пользовательское соглашение</a></div>
                            </li>
                            <li>
                                <div class="thumb-content"><a href="#.">Корпоративный сайт</a></div>
                            </li>
                        </ul>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <div class="footer-copyright">
        <div class="container">
            <div class="row">
                <div class="col-md-12 text-center">
                    <p>Сделано командой PINK CATS</p>
                </div>
            </div>
        </div>
    </div>
</div>


<script src="assets/js/script.js"></script>

<script>


    function yourFunction(){

        // если смотрим видео для слепых
        if(document.getElementById('switch_btn').checked) {
            $.ajax({
                type: "GET",
                url: "http://pinkcats.my.to:8080/api/get_video",
                dataType: "json",
                data: {
                    'film_id': 4,       // id фильма
                    'only_updated': 1,      // фильм для слепых
                    'metadata': 1            // получаем длину видео
                },
                complete: function (data) {
                    //data - то что возвращает api
                    if(data.responseText != 'Фильм еще не обработан'){

                        itime = (JSON.parse(data.responseText)).length;


                        var player = document.getElementById('player');
                        is_paused = document.getElementById('player').paused;   // проверяем стоит ли видео на паузе


                        videotime = player.currentTime;     // таймкод нашего видео

                        //console.log(document.getElementById("player").duration, itime);

                        // если наше видео короче нового
                        // вместо itime данные из data


                        if(itime && isNaN(document.getElementById("player").duration)){
                            document.getElementById('animation').style.display = 'none';
                            document.getElementById('video_body').style.display = 'block';
                        }

                        if ((itime && isNaN(document.getElementById("player").duration)) || Math.round(itime) > Math.round(document.getElementById("player").duration)) {
                            console.log(Math.round(itime) > Math.round(document.getElementById("player").duration));

                            document.getElementById('animation').style.display = 'none';
                            document.getElementById('video_body').style.display = 'block';

                            // гет запрос на получения видео из api
                            document.getElementById('path_to_video').src = 'http://pinkcats.my.to:8080/api/get_video?film_id=4&only_updated=1';
                            player.load();  // перезагружаем плеер

                            console.log(document.getElementById('path_to_video').src, videotime);

                            if(isNaN(videotime)){
                                player.currentTime = 1; // устанавливаем текущее время
                            }else{
                                player.currentTime = videotime; // устанавливаем текущее время
                            }

                            console.log(player.currentTime, is_paused, player);

                            // если видео было не на паузе, то запустить
                            if (!is_paused) {
                                player.play();
                            }

                            if(isNaN(is_paused)){
                                player.play();
                            }

                        }

                    }

                }
            });
        }



        setTimeout(yourFunction, 5000);  // 5000 - вызов каждый 5 секунд

    }

    yourFunction();

</script>


<audio id="sound"><source src="assets/audio/info_silero_kseniya.wav" type="audio/mp3"></audio>
<script>
    function playSound(sound) {
        var song = document.getElementById(sound);
        song.volume = 1;
        if (song.paused) {
            song.play();
        } else {
            song.pause();
        }
    }
</script>


<script>
    document.addEventListener('keyup', function(event){

        if(event.keyCode == 13){
            if(!document.getElementById('switch_btn').checked){
                document.getElementById('switch_btn').checked = true;
                checkAddress();
            }else if(document.getElementById('switch_btn').checked){
                document.getElementById('switch_btn').checked = false;
                checkAddress()
            }
        }

    });
</script>


</body>
</html>