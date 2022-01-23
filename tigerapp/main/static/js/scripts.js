/* populate feed with item cards */
function handleSearchResponse(response){
    $('#search_indicator').hide()
    $('#posts').html(response);
    }

/* reset both dates in search by date */
function dateClear(){
    $("#startfilter").val("");
    $("#endfilter").val("");
    getResults();
}

/* reset the search and sidebar */
function resetAll(){
    $('#sidebar').find('input:checkbox').prop('checked', false);
    $('input[name=time][value="desc"]').prop('checked', 'checked');
    $("#startfilter").val("");
    $("#endfilter").val("");
    getResults();
}

let request = null

/* dynamically display results after applying filters/search/sort */
function getResults(){

    /* url will populate feed with items matching filters/search/sort */
    let filters=build_filter_url()
    let url = '/' + ($("#title").text()).split(" ")[0].toLowerCase() + 'feed' + filters

    let title = ($("#title").text()).split(" ")[0].toLowerCase()
    
    if (title == 'hidden' || title == 'dashboard'){
        url = '/admin' + url
    }

    request = $.ajax({
        type: 'GET',
        url: url,
        success: handleSearchResponse
    });

}


function visibility(postId){

    postId = encodeURIComponent(postId)

    let filters = encodeURIComponent(build_filter_url())

    let url = '/post/'+ postId +'/togglevisibility' + '/' + ($("#title").text()).split(" ")[0].toLowerCase() + '?filters=' + filters

    if(request != null){
        request.abort()
    }

    request = $.ajax({
        type: 'POST',
        url: url,
        success: handleSearchResponse
    });

}

function toggleban(userid){

    postId = encodeURIComponent(userid)

    let filters = encodeURIComponent(build_filter_url())

    let url = '/user/'+ userid +'/toggleban' +'?filters=' + filters

    if(request != null){
        request.abort()
    }

    request = $.ajax({
        type: 'POST',
        url: url,
        success: handleSearchResponse
    });

}

function toggleadmin(userid){

    postId = encodeURIComponent(userid)

    let filters = encodeURIComponent(build_filter_url())

    let url = '/user/'+ userid +'/assignadmin' +'?filters=' + filters

    if(request != null){
        request.abort()
    }

    request = $.ajax({
        type: 'POST',
        url: url,
        success: handleSearchResponse
    });

}

/* build url query string using current filter/sort/search states. */
function build_filter_url(){

    /* feed loading icon */
    $('#search_indicator').show()
    if(request != null){
        request.abort()
    }

    /* get all checked tags */
    let currentTags = []
    let num_of_tags = 21 // hard-coded number of tags
    for(let i = 1; i < num_of_tags + 1; i++){
        if ($("#tag"+i).is(':checked')) {
            currentTags.push(i);
        }
    }

    /* search input */
    let keyword = $('#search').val()
    keyword = encodeURIComponent(keyword)
    let filters = '?keyword=' + keyword

    /* start and end dates from search by date */
    let startdate = $("#startfilter").val()
    let enddate = $("#endfilter").val()

    if(Date.parse(startdate) > Date.parse(enddate)){
        $("#endfilter").val($("#startfilter").val())
        $("#daterror").html('<div class="alert alert-danger alert-dismissible fade show" role="alert"> \
                <strong>Hey!</strong> End date must be after start date.\
                <button type="button" class="close" data-bs-dismiss="alert" aria-label="Close">\
                <span aria-hidden="true">&times;</span>\
                </button>\
                </div>');

        enddate=startdate
    }

    startdate = encodeURIComponent(startdate)
    enddate = encodeURIComponent(enddate)

    if (startdate != ""){
        filters += '&startdate=' + startdate
    }
    if (enddate != ""){
        filters += '&enddate=' + enddate
    }

    /* all checked tags */
    for(const tag of currentTags){
        filters += "&" + tag + "=" + tag
    }

    /* get sort by time radio button value */
    filters += "&time=" + $('input[name="time"]:checked').val()

    /* myposts: active vs history button value */
    if($("#btn_history").is(':checked')){
        filters += "&history=" + $("#btn_history").val()
    }

    /* myposts: lost/found filter check boxes */
    let lostChecked = $("#lostfilter").is(':checked')
    let foundChecked = $("#foundfilter").is(':checked')
    if((lostChecked && !foundChecked) || (!lostChecked && foundChecked)){
        let val = lostChecked ? $("#lostfilter").val() : $("#foundfilter").val()
        filters += "&lostfound=" + val
    }


    if($("#banned").is(':checked')){
        let val = $("#banned").val()
        filters += "&banned=" + val
    }

    if($("#adm").is(':checked')){
        let val = $("#adm").val()
        filters += "&admin=" + val
    }

    return filters
}

/* dynamically resolve a post*/
function resolvePost(postId){
    
    postId = encodeURIComponent(postId)

    /* url will resolve post and then reroute to display
    current page dynamically with current filters */
    let filters= encodeURIComponent(build_filter_url())
    let url = '/post/'+ postId +'/resolve'+'?filters=' + filters

    if(request != null){
        request.abort()
    }

    request = $.ajax({
        type: 'POST',
        url: url,
        success: handleSearchResponse
    });
}

/* dynamically unresolve a post*/
function unresolvePost(postId){
    
    postId = encodeURIComponent(postId)

    /* url will unresolve post and then reroute to display
    current page dynamically with current filters */
    let filters= encodeURIComponent(build_filter_url())
    let url = '/post/'+ postId +'/unresolve'+'?filters=' + filters

    if(request != null){
        request.abort()
    }

    request = $.ajax({
        type: 'POST',
        url: url,
        success: handleSearchResponse
    });
}

/* dynamically delete a post*/
function deletePost(postId){
    
    postId = encodeURIComponent(postId)

    /* url will unresolve post and then reroute to display
    current page dynamically with current filters */
    let filters= encodeURIComponent(build_filter_url())
    let url = '/post/'+ postId +'/delete'+'?filters=' + filters

    if(request != null){
        request.abort()
    }

    request = $.ajax({
        type: 'POST',
        url: url,
        success: handleSearchResponse
    });
}

/* dynamically renew a post*/
function renewPost(postId){
    
    postId = encodeURIComponent(postId)

    /* url will renew post and then reroute to display
    current page dynamically with current filters */
    let filters= encodeURIComponent(build_filter_url())
    let url = '/post/'+ postId +'/renew'+'?filters=' + filters

    if(request != null){
        request.abort()
    }

    request = $.ajax({
        type: 'POST',
        url: url,
        success: handleSearchResponse
    });
}

/* setup */
function setup(){
    getResults()
    $('#search').on('input', getResults)
}

$('document').ready(setup)