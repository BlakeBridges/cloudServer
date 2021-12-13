var jwt = null
function secure_get_with_token(endpoint, on_success_callback, on_fail_callback){
	xhr = new XMLHttpRequest();
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
	}
	function get_and_set_new_jwt(data){
		console.log(data);
		jwt  = data.token
		on_success_callback(data)
	}
	$.ajax({
		url: endpoint,
		type: 'GET',
		datatype: 'json',
		success: on_success_callback,
		error: on_fail_callback,
		beforeSend: setHeader
	});
}



function secure_post_with_token(endpoint, data_to_send, on_success_callback, on_fail_callback){
        xhr = new XMLHttpRequest();
        function setHeader(xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
        }
        function get_and_set_new_jwt(data){
                console.log(data);
                jwt  = data.token
                on_success_callback(data)
        }
        $.ajax({
                url: endpoint,
                type: 'POST',
                datatype: 'json',
		data: data_to_send,
                success: on_success_callback,
                error: on_fail_callback,
                beforeSend: setHeader
        });
}

function secure_file_upload(endpoint, data_to_send, on_success_callback, on_fail_callback)
{
	xhr = new XMLHttpRequest();
		
	xhr.upload.addEventListener('progress', function (e) {
        var file1Size = data_to_send;

        if (e.loaded <= file1Size) {
            var percent = Math.round(e.loaded / file1Size * 100);
            $('#progress-bar-file1').width(percent + '%').html(percent + '%');
        } 

        if(e.loaded == e.total){
            $('#progress-bar-file1').width(100 + '%').html(100 + '%');
        }
    	});   

        function setHeader(xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
	
        }

	$.ajax({
		//actual post
       		 url: endpoint,
        	type: "POST",
        	contentType:false,
        	processData: false,
        	cache: false,
        	data: data_to_send,
        	success: on_success_callback,
		error: on_fail_callback,
        	beforeSend: setHeader 

 });
}







