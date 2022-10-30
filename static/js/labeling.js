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
}

function Anti_Label(){
    document.location.href = '/manual_label_anti'
}

function Neutral_Label(){
    document.location.href = '/manual_label_neutral'
}

function News_Label(){
    document.location.href = '/manual_label_news'
}

function Switch_To_Model_Training(){
    document.location.href = '/training'
}

// show descriptive statistics and visualize the dataset, 
// show further information
function Switch_To_Model_Analysis(){
    document.location.href = '/analysis'
}