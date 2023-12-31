// save results when labeled
function Save_Results() {    
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}
// load next tweet when "next-tweet"-button on labeling page is clicked
function Next_Tweet(){
    document.location.href = '/next_tweet'
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}
// load next previous when "previous-tweet"-button on labeling page is clicked
function Previous_Tweet(){
    document.location.href = '/previous_tweet'
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}
// update progress bar on labeling page
function move() {
    var elem = document.getElementById("myBar");
    var width = document.getElementById("myBar").textContent;
    width = parseFloat(width);
    var id = setInterval(frame, 10);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            elem.style.width = width + '%';
        }
    }
}

// save label in dataset and color elements on labeling page accordingly
function Pro_Label(){
    document.location.href = '/manual_label_pro';
    pro_symbol = document.getElementById('pro-symbol');
    pro_symbol.style.fill = "rgb(27, 149, 224)";
    
    var pro_labeltext = document.getElementById("pro_labeltext");
    pro_labeltext.style.background = "rgb(27, 149, 224)";

    // grey for the others
    neutral_symbol = document.getElementById('neutral-symbol');
    anti_symbol = document.getElementById('anti-symbol');
    news_symbol = document.getElementById('news-symbol');
    news_symbol_2 = document.getElementById('news-symbol-2');

    neutral_symbol.style.fill = "rgb(101, 119, 134)";
    anti_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol_2.style.fill = "rgb(101, 119, 134)";

    var anti_labeltext = document.getElementById("anti_labeltext");
    var neutral_labeltext = document.getElementById("neutral_labeltext");
    var news_labeltext = document.getElementById("news_labeltext");

    anti_labeltext.style.background = "none";
    neutral_labeltext.style.background = "none";
    news_labeltext.style.background = "none";

    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}
// save label in dataset and color elements on labeling page accordingly
function Anti_Label(){
    document.location.href = '/manual_label_anti';
    anti_symbol = document.getElementById('anti-symbol');
    anti_symbol.style.fill = "rgb(23, 191, 99)";
    
    var anti_labeltext = document.getElementById("anti_labeltext");
    anti_labeltext.style.background = "rgb(23, 191, 99)";
    //anti_symbol.style.opacity = "0.1";

    // grey for the others
    neutral_symbol = document.getElementById('neutral-symbol');
    news_symbol = document.getElementById('news-symbol');
    news_symbol_2 = document.getElementById('news-symbol-2');
    pro_symbol = document.getElementById('pro-symbol');

    neutral_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol_2.style.fill = "rgb(101, 119, 134)";
    pro_symbol.style.fill = "rgb(101, 119, 134)";

    var pro_labeltext = document.getElementById("pro_labeltext");
    var neutral_labeltext = document.getElementById("neutral_labeltext");
    var news_labeltext = document.getElementById("news_labeltext");

    pro_labeltext.style.background = "none";
    neutral_labeltext.style.background = "none";
    news_labeltext.style.background = "none";

    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}
// save label in dataset and color elements on labeling page accordingly
function Neutral_Label(){
    document.location.href = '/manual_label_neutral';
    neutral_symbol = document.getElementById('neutral-symbol');
    neutral_symbol.style.fill = "rgb(215, 42, 94)";

    var neutral_labeltext = document.getElementById("neutral_labeltext");
    neutral_labeltext.style.background = "rgb(215, 42, 94)";

    // grey for the others
    news_symbol = document.getElementById('news-symbol');
    news_symbol_2 = document.getElementById('news-symbol-2');
    anti_symbol = document.getElementById('anti-symbol');
    pro_symbol = document.getElementById('pro-symbol');

    news_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol_2.style.fill = "rgb(101, 119, 134)";
    anti_symbol.style.fill = "rgb(101, 119, 134)";
    pro_symbol.style.fill = "rgb(101, 119, 134)";

    var pro_labeltext = document.getElementById("pro_labeltext");
    var anti_labeltext = document.getElementById("anti_labeltext");
    var news_labeltext = document.getElementById("news_labeltext");

    pro_labeltext.style.background = "none";
    anti_labeltext.style.background = "none";
    news_labeltext.style.background = "none";

    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}
// save label in dataset and color elements on labeling page accordingly
function News_Label(){
    document.location.href = '/manual_label_news';
    news_symbol = document.getElementById('news-symbol');
    news_symbol.style.fill = "rgb(27, 149, 224)";
    news_symbol_2 = document.getElementById('news-symbol-2');
    news_symbol_2.style.fill = "rgb(27, 149, 224)";

    var news_labeltext = document.getElementById("news_labeltext");
    news_labeltext.style.background = "rgb(27, 149, 224)";

    // grey for the others
    neutral_symbol = document.getElementById('neutral-symbol');
    anti_symbol = document.getElementById('anti-symbol');
    pro_symbol = document.getElementById('pro-symbol');
    
    neutral_symbol.style.fill = "rgb(101, 119, 134)";
    anti_symbol.style.fill = "rgb(101, 119, 134)";
    pro_symbol.style.fill = "rgb(101, 119, 134)";

    var pro_labeltext = document.getElementById("pro_labeltext");
    var anti_labeltext = document.getElementById("anti_labeltext");
    var neutral_labeltext = document.getElementById("neutral_labeltext");

    pro_labeltext.style.background = "none";
    anti_labeltext.style.background = "none";
    neutral_labeltext.style.background = "none";

    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

function Switch_To_Model_Training(){
    document.location.href = '/loading_screen'
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

function delete_row(){
    document.location.href = '/delete_row'
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}
// show descriptive statistics and visualize the dataset, 
// show further information
function Switch_To_Model_Analysis(){
    document.location.href = '/analysis'
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}
// Button to go to Labeling page
function Switch_To_Labeling(){
    document.location.href = '/labeling'
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

// download option
function download_csv() {
    var name = document.getElementById("which_dataset").value;        
    if (name) {
        window.location = '/download_csv?dataset=' + name;
     }
     return false;
}

// delete option
function delete_csv() {
    var name = document.getElementById("which_dataset").value;        
    if (name) {
        window.location = '/delete_csv?dataset=' + name;
     }
     return false;
}

// show pop-up when message is flashed from app.py
function show_pop_up() {
    var name = document.getElementById("pop_up");
    name.className = "show";
    setTimeout(function(){ name.className = name.className.replace("show", ""); }, 3000);
}