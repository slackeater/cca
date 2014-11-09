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
	$("#downCont").fadeIn("slow")
}
