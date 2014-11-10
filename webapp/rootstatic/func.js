/* === User Info === */
function showUserInfo(platform){
	$("#wait0").fadeIn("slow");
	$("#userInfoError").fadeOut("slow");
	Dajaxice.cloudservice.userInfo(infoCallBack,{'tokenID':tVal(), 'platform':platform})
}

function infoCallBack(data){
	Dajax.process(data)
	$("#wait0").fadeOut("slow");
	$("#accountTab").fadeIn("slow");
	$("#userInfoError").fadeIn("slow");
}
/* End */

/* ==== Analysis ==== */

function startMetaAnalysis(update, platform){
	$("#wait1").fadeIn("slow");
	$("#metaAnalysisError").fadeOut("slow");
	Dajaxice.cloudservice.metadataAnalysis(analysisCallBack,{'tokenID': tVal(), 'update': update, 'platform': platform});
}

// callback for analysis
function analysisCallBack(data){
 	Dajax.process(data)
	$("#wait1").fadeOut("slow");
	$("#metaAnalysis").fadeIn("slow");
	$("#metaAnalysisError").fadeIn("slow");
}

/* === Search === */

function startRes(platform){
	$("#wait2").fadeIn("slow");
	$("#searchError").fadeOut("slow");
	Dajaxice.cloudservice.searchMetaData(resCallBack, {'platform': platform, 'tokenID': tVal(), 'form': $("#searchForm").serialize(true)})
}

function resCallBack(data){
	Dajax.process(data)
	$("#wait2").fadeOut("slow");
	$("#searchRes").fadeIn("slow");
	$("#searchError").fadeIn("slow");
}

function showFile(id,platform){
	$("#searchError").fadeOut("slow");
	Dajaxice.cloudservice.fileInfo(showCallBack,{'platform': platform,'tokenID': tVal(), 'id': id})
}

function showCallBack(data){
	Dajax.process(data)
	$("#searchResult").fadeOut("slow")
	$("#fileRevisionContainer").fadeIn("slow")
	$("#searchError").fadeIn("slow");
}

function showRevision(id,platform){
	$("#revisionWait").fadeIn("slow")
	Dajaxice.cloudservice.fileRevision(revCallBack,{'platform':platform,'id': id, 'tokenID': tVal()})
}

function revCallBack(data){
	Dajax.process(data)
	$("#revisionWait").fadeOut("slow")
	$("#revisionHistory").fadeIn("slow")
}

/* End */

/* === Downloader === */ 

function showDownload(platform){
	Dajaxice.cloudservice.showDownload(showDownCallBack,{'platform':platform,'tokenID':tVal()})
}

function showDownCallBack(data){
	Dajax.process(data)
	$("#downError").fadeIn("slow")
	$("#downCont").fadeIn("slow")
}

function startForegroundDownload(platform){
	$("#downError").fadeOut("slow")
	Dajaxice.cloudservice.startForegroundDownload(foregroundCallBack,{'platform':platform,'tokenID':tVal()})
}

function foregroundCallBack(data){
	Dajax.process(data)
	$("#downStatus").fadeIn("slow")
	$("#downError").fadeIn("slow")
		alert(data[0].val)
	if(data[0].val == "true"){
		$("form#downListForm :input[type=hidden]").each(function(){
			var input = $(this)
			Dajaxice.cloudservice.downloadFile(downFileCallBack,{'platform':$("#p").val(),'fileName': input.val()})
		});

	}
}

function downFileCallBack(data){
	//File processing has gone good
	if(data[0].val == "correct"){
		html = parseInt($("#file").text())
		totalLen = $("#progress").width()
		nowFileLen = $("#progressLen").width()
		totalFile = parseInt($("#total").text());

		//block length
		blockLen = totalLen / totalFile

		//add the block to the current progress width
		$("#progressLen").width(nowFileLen+blockLen)

		//update file count
		tot = html + 1
		$("#file").text(tot)

		//we reached the end 
		if (tot == totalFile){
			oldText = $("#fileDownStatus").text()
			 $("#fileDownStatus").html(oldText + "<p>Completed</p>")
			 $("#fileDownStatus").fadeIn("slow")
			 $("#waitDown").fadeOut("slow")
			 $("#downBnt").fadeIn("slow")
		}
	}
	else{
		cont = data[0].val
		oldText = $("#fileDownStatus").text()
		$("#fileDownStatus").text(oldText+cont)
		$("#fileDownStatus").fadeIn("slow")
	}
}


/* End */
