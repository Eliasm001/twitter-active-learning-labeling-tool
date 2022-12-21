function Save_Results() {    
    $.getJSON('/save_results',
        function(data) {
        //just call save_results
    });
    return false;
}

function Next_Tweet(){
    document.location.href = '/next_tweet'
}

function Previous_Tweet(){
    document.location.href = '/previous_tweet'
}

function Pro_Label(){
    document.location.href = '/manual_label_pro'
    pro_symbol = document.getElementById('pro-symbol');
    pro_symbol.style.fill = "rgb(27, 149, 224)";

    // grey for the others
    neutral_symbol = document.getElementById('neutral-symbol');
    anti_symbol = document.getElementById('anti-symbol');
    news_symbol = document.getElementById('news-symbol');

    neutral_symbol.style.fill = "rgb(101, 119, 134)";
    anti_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol.style.fill = "rgb(101, 119, 134)";
}

function Anti_Label(){
    document.location.href = '/manual_label_anti'
    anti_symbol = document.getElementById('anti-symbol');
    anti_symbol.style.fill = "rgb(23, 191, 99)";
    //anti_symbol.style.opacity = "0.1";

    // grey for the others
    neutral_symbol = document.getElementById('neutral-symbol');
    news_symbol = document.getElementById('news-symbol');
    pro_symbol = document.getElementById('pro-symbol');

    neutral_symbol.style.fill = "rgb(101, 119, 134)";
    news_symbol.style.fill = "rgb(101, 119, 134)";
    pro_symbol.style.fill = "rgb(101, 119, 134)";
}

function Neutral_Label(){
    document.location.href = '/manual_label_neutral'
    neutral_symbol = document.getElementById('neutral-symbol');
    neutral_symbol.style.fill = "rgb(215, 42, 94)";

    // grey for the others
    news_symbol = document.getElementById('news-symbol');
    anti_symbol = document.getElementById('anti-symbol');
    pro_symbol = document.getElementById('pro-symbol');

    news_symbol.style.fill = "rgb(101, 119, 134)";
    anti_symbol.style.fill = "rgb(101, 119, 134)";
    pro_symbol.style.fill = "rgb(101, 119, 134)";
}

function News_Label(){
    document.location.href = '/manual_label_news'
    news_symbol = document.getElementById('news-symbol');
    news_symbol.style.fill = "rgb(27, 149, 224)";
    news_symbol = document.getElementById('news-symbol-2');
    news_symbol.style.fill = "rgb(27, 149, 224)";

    // grey for the others
    neutral_symbol = document.getElementById('neutral-symbol');
    anti_symbol = document.getElementById('anti-symbol');
    pro_symbol = document.getElementById('pro-symbol');

    neutral_symbol.style.fill = "rgb(101, 119, 134)";
    anti_symbol.style.fill = "rgb(101, 119, 134)";
    pro_symbol.style.fill = "rgb(101, 119, 134)";
}

function Switch_To_Model_Training(){
    document.location.href = '/training'
}

// show descriptive statistics and visualize the dataset, 
// show further information
function Switch_To_Model_Analysis(){
    document.location.href = '/analysis'
}