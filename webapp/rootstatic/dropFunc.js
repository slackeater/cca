/* ==== Analysis ==== */

function showCont(){
	$("#wait").fadeIn("slow");
	Dajaxice.dropcloud.analyzeDropMetaData(analysisCallBack,{'resName': 'analysisRes','tokenID': vars['t']});
}

// callback for analysis
function analysisCallBack(data){
	Dajax.process(data)
	$("#wait").fadeOut("slow");
	$("#analysisRes").fadeIn("slow");
}

/* End */

/* ==== Meta Research ==== */

function startRes(){
	$("#wait2").fadeIn("slow");
	Dajaxice.dropcloud.searchMetaData(searchCallBack,{'form':$('#searchForm').serialize(true), 'tokenID': vars['t']});
}

// callback for meta search
function searchCallBack(data){
	Dajax.process(data);
	$("#wait2").fadeOut("slow");
	$("#searchRes").fadeIn("slow");
}

/* End */

/* ==== File list to download ==== */

function getDownloadList(){
	$("#wait3").fadeIn("slow");
	Dajaxice.dropcloud.getDownloadList(downCallBack,{'tokenID': vars['t']});
}

// callback for download list
function downCallBack(data){
	Dajax.process(data);
	$("#wait3").fadeOut("slow");
	$("#downList").fadeIn("slow");
}

/* End */

/* ==== Download ==== */

function wrapDownload(){
	Dajaxice.dropcloud.downloadWrapper(wrapperCallBack,{'tokenID': vars['t']});
}

function wrapperCallBack(data){
	if (data[0].val == "true")
		downloadFiles();
}


function downloadFiles(){
	$("#downBtn").fadeOut("slow");
	$("#waitDown").fadeIn("slow");
	$("#progressLen").width(0);
	$("#file").text(0);

	$("form#downListForm :input[type=hidden]").each(function(){
		var input = $(this);
		Dajaxice.dropcloud.downloadFile(downFileCallBack,{'fileName': input.val()});
	});
}

//callback for download of files
function downFileCallBack(data){
	if (data[0].val == "correct") {
		html = parseInt($("#file").text());
		totalLen = $("#progress").width();
		nowFileLen = $("#progressLen").width();
		totalFile = parseInt($("#total").text());
		
		//block length
		blockLen = totalLen / totalFile;

		//add the block to the current progress width
		$("#progressLen").width(nowFileLen+blockLen);
		
		tot = html + 1;
		$("#file").text(tot);
		
		if (tot == totalFile){
			oldText = $("#fileDownStatus").text();
			$("#fileDownStatus").html(oldText + "<p>Completed</p>");
			$("#fileDownStatus").fadeIn("slow");
			$("#waitDown").fadeOut("slow");
			$("#downBtn").fadeIn("slow");
		}
	}
	else{
		cont = data[0].val;
		oldText = $("#fileDownStatus").text();
		$("#fileDownStatus").text(oldText + cont);
		$("#fileDownStatus").fadeIn("slow");
	}	
}

/* End */

/* ==== Hash comparator === */

function compareHash(){
	Dajaxice.dropcloud.comparator(Dajax.process,{'tokenID': vars['t']});
}

/* End */

/* === Folder === */

function fold(cnt){
	$(cnt).fadeToggle("fast", "linear");
}

/* End */

/* === Revisioner === */

function showFile(name){
	$("#searchResult").fadeOut("slow", "linear");
	$("#revSpinner").fadeIn("slow");
	Dajaxice.dropcloud.fileRevisioner(showFileCallBack,{'tokenID': vars['t'], 'fileName': name});
}

function showFileCallBack(data){
	$("#fileRevisionContainer").fadeIn("fast", "linear");
	$("#revSpinner").fadeOut("slow");
	Dajax.process(data)
}

function backToSearch(){
	$("#fileRevisionContainer").fadeOut("fast", "linear");
	$("#searchResult").fadeIn("fast", "linear");
}
/* End */

