function Callback_Startbutton() {
    document.getElementById("StartB").textContent = "CLICK"
    document.location.href = '/labeling'
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