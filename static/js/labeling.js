function Save_Results() {    
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

function Next_Tweet(){
    document.location.href = '/next_tweet'
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

function Previous_Tweet(){
    document.location.href = '/previous_tweet'
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

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


function Pro_Label(){
    document.location.href = '/manual_label_pro'
    pro_symbol = document.getElementById('pro-symbol');
    pro_symbol.style.fill = "rgb(27, 149, 224)";

    // grey for the others
    neutral_symbol = document.getElementById('neutral-symbol');
    anti_symbol = document.getElementById('anti-symbol');
    news_symbol = document.getElementById('news-symbol');
    news_symbol_2 = document.getElementById('news-symbol-2');

    neutral_symbol.style.fill = "rgb(101, 119, 134)";
    anti_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol_2.style.fill = "rgb(101, 119, 134)";

    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

function Anti_Label(){
    document.location.href = '/manual_label_anti'
    anti_symbol = document.getElementById('anti-symbol');
    anti_symbol.style.fill = "rgb(23, 191, 99)";
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

    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

function Neutral_Label(){
    document.location.href = '/manual_label_neutral'
    neutral_symbol = document.getElementById('neutral-symbol');
    neutral_symbol.style.fill = "rgb(215, 42, 94)";

    // grey for the others
    news_symbol = document.getElementById('news-symbol');
    news_symbol_2 = document.getElementById('news-symbol-2');
    anti_symbol = document.getElementById('anti-symbol');
    pro_symbol = document.getElementById('pro-symbol');

    news_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol_2.style.fill = "rgb(101, 119, 134)";
    anti_symbol.style.fill = "rgb(101, 119, 134)";
    pro_symbol.style.fill = "rgb(101, 119, 134)";

    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

function News_Label(){
    document.location.href = '/manual_label_news'
    news_symbol = document.getElementById('news-symbol');
    news_symbol.style.fill = "rgb(27, 149, 224)";
    news_symbol_2 = document.getElementById('news-symbol-2');
    news_symbol_2.style.fill = "rgb(27, 149, 224)";

    // grey for the others
    neutral_symbol = document.getElementById('neutral-symbol');
    anti_symbol = document.getElementById('anti-symbol');
    pro_symbol = document.getElementById('pro-symbol');

    neutral_symbol.style.fill = "rgb(101, 119, 134)";
    anti_symbol.style.fill = "rgb(101, 119, 134)";
    pro_symbol.style.fill = "rgb(101, 119, 134)";

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

// show pop-up when dataset is created
function show_created() {
    if("{{dataset_created}}" == "True"){
        var name = document.getElementById("created_pop_up");
        name.className = "show";    
        setTimeout(function(){ name.className = ""; }, 3000);
    }
    "{{dataset_created}}" = "False"
}

// show pop-up when there is no previous tweet
function show_first_tweet() {
    var name = document.getElementById("first_tweet_pop_up");
    name.className = "show";    
    setTimeout(function(){ name.className = ""; }, 3000);
}

// show pop-up when there is no next tweet
function show_first_tweet() {
    var name = document.getElementById("first_tweet_pop_up");
    name.className = "show";    
    setTimeout(function(){ name.className = ""; }, 3000);
}