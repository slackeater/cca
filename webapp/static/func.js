/* ==== Analysis ==== */

function startMetaAnalysis(){
	$("#wait1").fadeIn("slow")
	$("#metaAnalysisError").fadeOut("slow")
	Dajaxice.cloudservice.metadataAnalysis(analysisCallBack,{'tokenID': tVal(),'cloudItem': iVal()})
}

function analysisCallBack(data){
 	Dajax.process(data)
	$("#wait1").fadeOut("slow")
	$("#metaAnalysis").fadeIn("slow")
	$("#metaAnalysisError").fadeIn("slow")
}

/* === Search === */

function startRes(start){
	$("#wait2").fadeIn("slow");
	$("#searchError").fadeOut("slow");
	Dajaxice.cloudservice.searchMetaData(resCallBack, {'cloudItem': iVal(),'tokenID': tVal(), 'form': $("#searchForm").serialize(true),'start':start})
}

function resCallBack(data){
	Dajax.process(data)
	$("#wait2").fadeOut("slow");
	$("#searchRes").fadeIn("slow");
	$("#searchError").fadeIn("slow");
}

function showFile(id){
	$("#searchError").fadeOut("slow");
	Dajaxice.cloudservice.fileInfo(showCallBack,{'cloudItem': iVal(),'tokenID': tVal(), 'id': id})
}

function showCallBack(data){
	Dajax.process(data)
	$("#searchResult").fadeOut("slow")
	$("#fileRevisionContainer").fadeIn("slow")
	$("#searchError").fadeIn("slow");
}

function showRevision(id){
	$("#revisionWait").fadeIn("slow")
	Dajaxice.cloudservice.fileRevision(revCallBack,{'fId': id, 'tokenID': tVal(),'cloudItem': iVal()})
}

function revCallBack(data){
	Dajax.process(data)
	$("#revisionWait").fadeOut("slow")
	$("#revisionHistory").fadeIn("slow")
}

/* End */
