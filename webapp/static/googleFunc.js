/* ==== Analysis ==== */

function startMetaAnalysis(t,update, platform){
	$("#wait1").fadeIn("slow");
	$("#metaAnalysisError").fadeOut("slow");
	Dajaxice.cloudservice.metadataAnalysis(analysisCallBack,{'tokenID': t, 'update': update, 'platform': platform});
}

// callback for analysis
function analysisCallBack(data){
 	Dajax.process(data)
	$("#wait1").fadeOut("slow");
	$("#metaAnalysis").fadeIn("slow");
	$("#metaAnalysisError").fadeIn("slow");
}

/* === Search === */

function startRes(t,platform){
	$("#wait2").fadeIn("slow");
	$("#searchError").fadeOut("slow");
	Dajaxice.gdrivecloud.searchMetaData(resCallBack, {'platform': platform, 'tokenID': t, 'form': $("#searchForm").serialize(true)})
}

function resCallBack(data){
	Dajax.process(data)
	$("#wait2").fadeOut("slow");
	$("#searchRes").fadeIn("slow");
	$("#searchError").fadeIn("slow");
}

function showFile(t,id){
	//loader
	$("#searchError").fadeOut("slow");
	Dajaxice.gdrivecloud.fileInfo(showCallBack,{'tokenID': t, 'id': id})
}

function showCallBack(data){
	Dajax.process(data)
	$("#searchResult").fadeOut("slow")
	$("#fileRevisionContainer").fadeIn("slow")
	$("#searchError").fadeIn("slow");
}

function showRevision(t,id){
	$("#revisionHistory").fadeIn("slow")
	Dajaxice.gdrivecloud.fileRevision(Dajax.process,{'id': id, 'tokenID': t, 'importID': vars['i']})
}

/* End */
